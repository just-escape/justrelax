import Vue from 'vue'
import Vuex from 'vuex'

import i18n from '@/locales.js'
import router from '@/router.js'

import lightStore from '@/store/lightStore.js'
import menuLogStore from '@/store/menuLogStore.js'
import lightLogStore from '@/store/lightLogStore.js'
import difficultyStore from '@/store/difficultyStore.js'
import menuStore from '@/store/menuStore.js'
import progressionStore from '@/store/progressionStore.js'

Vue.use(Vuex)

const publishSubscribeService = new Vuex.Store({
  state: {
    name: "synchronizer",
    subscriptionChannels: [],
    publicationChannel: undefined,
  },
  mutations: {
    addSubscriptionChannel (state, subscriptionChannel) {
      state.subscriptionChannels.push(subscriptionChannel)
    },
    setPublicationChannel (state, publicationChannel) {
      state.publicationChannel = publicationChannel
    },
    // eslint-disable-next-line
    SOCKET_ONOPEN (state, event) {
      Vue.prototype.$socket = event.currentTarget

      let query = JSON.parse(JSON.stringify(router.app.$route.query))

      if (query.name !== undefined) {
        state.name = query.name
      }

      for (let channel of state.subscriptionChannels) {
        let subscribeEvent = {
          action: "subscribe",
          channel: channel,
        }
        Vue.prototype.$socket.send(JSON.stringify(subscribeEvent))
      }
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
      let event = message.event

      if (event.category === 'reset') {
        // Reload page
        router.go()
      } else if (event.category === 'set_difficulty') {
        difficultyStore.commit('setDifficulty', event.difficulty)
      } else if (event.category === 'set_locale') {
        let query = JSON.parse(JSON.stringify(router.app.$route.query))
        if (event.locale == 'fr') {
          if (i18n.locale != 'fr') {
            query.locale = 'fr'
            router.push({path: '/', query: query})
          }
          i18n.locale = 'fr'
        } else {
          if (i18n.locale != 'en') {
            query.locale = 'en'
            router.push({path: '/', query: query})
          }
          i18n.locale = 'en'
        }
      } else if (event.category === 'menu_log') {
        let logMessage = event.message
        let level = event.level
        let useLocale = event.use_locale
        menuLogStore.commit('processLog', {logMessage, level, useLocale})
      } else if (event.category === 'light_log') {
        let logMessage = event.message
        let level = event.level
        let useLocale = event.use_locale
        lightLogStore.commit('processLog', {logMessage, level, useLocale})
      } else if (event.category === 'set_menu_cursor_position') {
        menuStore.commit('setMenuCursorPosition', event.position)
      } else if (event.category === 'force_menu_success') {
        menuStore.commit('forceSuccess')
      } else if (event.category === 'force_light_success') {
        progressionStore.commit('setLightServiceSuccess')
      } else if (event.category === 'load_cell') {
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
      } else if (event.category === 'play_ms_pepper_overlay_video') {
        progressionStore.commit('playMsPepperOverlayVideo', event.video_id)
      } else if (event.category === 'stop_ms_pepper_overlay_video') {
        progressionStore.commit('stopMsPepperOverlayVideo')
      } else if (event.category === 'display_selectable_areas') {
        menuStore.commit('setDisplaySelectableAreas', event.display)
      } else if (event.category === 'display_graduations') {
        menuStore.commit('setDisplayGraduations', event.display)
      } else if (event.category === 'display_graduation_texts') {
        menuStore.commit('setDisplayGraduationTexts', event.display)
      } else if (event.category === 'set_auto_validate_dishes') {
        menuStore.commit('setAutoValidateDishes', event.value)
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
    publish (state, event) {
      event.from = state.name
      let json = JSON.stringify({action: "publish", channel: state.publicationChannel, event: event})
      Vue.prototype.$socket.send(json)
    },
  },
})

export default publishSubscribeService
