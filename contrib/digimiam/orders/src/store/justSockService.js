import Vue from 'vue'
import Vuex from 'vuex'

import i18n from '@/locales.js'
import router from '@/router.js'

import progressionStore from '@/store/progressionStore.js'

Vue.use(Vuex)

const justSockService = new Vuex.Store({
  mutations: {
    // eslint-disable-next-line
    SOCKET_ONOPEN (state, event) {
      Vue.prototype.$socket = event.currentTarget
      let iamMessage = {
        message_type: "IAM",
        client_type: "node",
        channel: "digimiam1",
        name: "orders",
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
      if (message.message_type !== 'EVENT') {
        return
      }

      let event = message.event
      if (event.category === 'reset') {
        // Reload page
        router.go()
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
      } else if (event.category === 'play_overlay_video') {
        progressionStore.commit('playOverlayVideo', event.video_id)
      } else if (event.category === 'stop_overlay_video') {
        progressionStore.commit('stopOverlayVideo')
      } else if (event.category === 'set_ventilation_panel_round') {
        progressionStore.commit('setRound', event.round)
      } else if (event.category === 'set_documentation_visibility') {
        progressionStore.commit('setDocumentationVisibility', event.show)
      } else if (event.category === 'set_marmitron_visibility') {
        progressionStore.commit('setMarmitronVisibility', event.show)
      } else if (event.category === 'set_restaurant_status') {
        progressionStore.commit('setRestaurantStatus', event.closed)
      } else if (event.category === 'display_danger_window') {
        progressionStore.commit('displayDangerWindow')
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
    // eslint-disable-next-line
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
