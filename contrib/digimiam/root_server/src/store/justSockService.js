import Vue from 'vue'
import Vuex from 'vuex'

import i18n from '@/locales.js'
import router from '@/router.js'

import businessStore from '@/store/businessStore.js'

Vue.use(Vuex)

const justSockService = new Vuex.Store({
  mutations: {
    // eslint-disable-next-line
    SOCKET_ONOPEN (state, event) {
      Vue.prototype.$socket = event.currentTarget

      let query = JSON.parse(JSON.stringify(router.app.$route.query))

      let name = "root_server"
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
      if (event.type == 'reset') {
        // Reload page
        router.go()
      } else if (event.type == 'l10n') {
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
      } else if (event.category === 'display_password_window') {
        businessStore.commit('displayPasswordWindow')
      } else if (event.category === 'final_animation') {
        businessStore.commit('finalAnimation')
      } else if (event.category === 'display_danger_window') {
        businessStore.commit('displayDangerWindow')
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
