import Vue from 'vue'
import Vuex from 'vuex'

import i18n from '@/locales.js'
import router from '@/router.js'

import l10nStore from '@/store/l10nStore.js'
import lightStore from '@/store/lightStore.js'
import logStore from '@/store/logStore.js'

Vue.use(Vuex);

const justSockService = new Vuex.Store({
  mutations: {
    // eslint-disable-next-line
    SOCKET_ONOPEN (state, event) {
      Vue.prototype.$socket = event.currentTarget
      Vue.prototype.$socket.send(
        JSON.stringify(
          {
            "type": "IAM",
            "content": {
              "client_type": "$node",
              "channel": "digimiam1",
              "name": "synchronizer",
            }
          }
        )
      )
    },
    SOCKET_ONCLOSE (state, event) {
      // eslint-disable-next-line
      console.error(state, event)
    },
    SOCKET_ONERROR (state, event) {
      // eslint-disable-next-line
      console.error(state, event)
    },
    SOCKET_ONMESSAGE (state, message) {
      var msg = JSON.parse(message.data)
      if (msg.type != 'MSG') {
        return
      }

      var content = msg.content
      if (content.type == 'reset') {
        // Reload page
        router.go()
      } else if (content.type == 'l10n') {
        if (content.lang == 'fr') {
          if (i18n.locale != 'fr') {
            router.push({path: '/', query: {'lang': 'fr'}})
          }
          i18n.locale = 'fr'
          l10nStore.commit('setLang', 'fr')
        } else {
          if (i18n.locale != 'en') {
            router.push({path: '/', query: {'lang': 'en'}})
          }
          i18n.locale = 'en'
          l10nStore.commit('setLang', 'en')
        }
      } else if (content.type == 'log') {
        var logLevel = content.level
        var logMessage = content.message
        logStore.commit('processEventLog', {logLevel, logMessage})
      } else if (content.type == 'sensor') {
        var sensorId = content['sensor_id']
        var activated = content.activated
        lightStore.dispatch('toggleSensor', {sensorId, activated})
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
    sendToGateway (state, message) {
      Vue.prototype.$socket.send(message)
    },
  },
  actions: {
    sendToGateway (context, message) {
      context.commit('sendToGateway', message)
    }
  }
})

export default justSockService
