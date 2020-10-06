import Vue from 'vue'
import Vuex from 'vuex'

import i18n from '@/locales.js'
import router from '@/router.js'

import lightStore from '@/store/lightStore.js'
import logStore from '@/store/logStore.js'
import difficultyStore from '@/store/difficultyStore.js'
import menuStore from '@/store/menuStore.js'
import progressionStore from '@/store/progressionStore.js'

Vue.use(Vuex)

const justSockService = new Vuex.Store({
  mutations: {
    // eslint-disable-next-line
    SOCKET_ONOPEN (state, event) {
      Vue.prototype.$socket = event.currentTarget

      let query = JSON.parse(JSON.stringify(router.app.$route.query))

      let name = "synchronizer"
      if (query.name !== undefined) {
        name = query.name
      }

      let channel = "digimiam1"
      if (query.channel !== undefined) {
        channel = query.channel
      }

      let iamMessage = {
        message_type: "IAM",
        client_type: "node",
        channel: channel,
        name: name,
      }
      Vue.prototype.$socket.send(JSON.stringify(iamMessage))
    },
    SOCKET_ONCLOSE (state, event) {
      // eslint-disable-next-line
      console.error(state, event)
    },
    SOCKET_ONERROR (state, event) {
      // eslint-disable-next-line
      console.error(state, event)
    },
    SOCKET_ONMESSAGE (state, rawMessage) {
      let message = JSON.parse(rawMessage.data)
      if (message.message_type != 'EVENT') {
        return
      }

      let event = message.event
      if (event.category == 'reset') {
        // Reload page
        router.go()
      } else if (event.category == 'set_difficulty') {
        difficultyStore.commit('setDifficulty', event.difficulty)
      } else if (event.category == 'l10n') {
        let query = JSON.parse(JSON.stringify(router.app.$route.query))
        if (event.lang == 'fr') {
          if (i18n.locale != 'fr') {
            query.lang = 'fr'
            router.push({path: '/', query: query})
          }
          i18n.locale = 'fr'
        } else {
          if (i18n.locale != 'en') {
            query.lang = 'en'
            router.push({path: '/', query: query})
          }
          i18n.locale = 'en'
        }
      } else if (event.category == 'log') {
        let logMessage = event.message
        let level = event.level
        let useLocale = event.use_locale
        logStore.commit('processLog', {logMessage, level, useLocale})
      } else if (event.category == 'set_menu_cursor_position') {
        menuStore.commit('setMenuCursorPosition', event.position)
      } else if (event.category == 'force_menu_success') {
        menuStore.commit('forceSuccess')
      } else if (event.category == 'load_cell') {
        let color = event['color']
        let activated = event.activated
        lightStore.dispatch('toggleColor', {color, activated})
      } else if (event.category === 'restaurant_in_manual_mode') {
        lightStore.commit('setRestaurantInManualMode')
      } else if (event.category === 'display_danger_window') {
        progressionStore.commit('displayDangerWindow')
      } else if (event.category === 'play_overlay_video') {
        progressionStore.commit('playOverlayVideo', event.video_id)
      } else if (event.category === 'stop_overlay_video') {
        progressionStore.commit('stopOverlayVideo')
      }
    },
    SOCKET_RECONNECT (state, count) {
      // eslint-disable-next-line
      console.info(state, count)
    },
    // eslint-disable-next-line
    SOCKET_RECONNECT_ERROR (state) {
      // eslint-disable-next-line
      console.error("Reconnect error")
    },
    sendEvent (state, event) {
      let message = {
        message_type: "EVENT",
        event: event,
      }
      let jsonMessage = JSON.stringify(message)
      Vue.prototype.$socket.send(jsonMessage)
    },
  },
})

export default justSockService
