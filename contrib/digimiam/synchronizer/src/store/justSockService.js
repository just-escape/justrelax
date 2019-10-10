import Vue from 'vue'
import Vuex from 'vuex'
import LightStore from '@/store/LightStore.js'
import LogStore from '@/store/LogStore.js'

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
      var event = JSON.parse(message.data)
      var content = event.content
      if (content.type == 'log') {
        var logLevel = content.level
        var logMessage = content.message
        LogStore.commit('processEventLog', {logLevel, logMessage})
      } else if (content.type == 'sensor') {
        var sensorId = content['sensor_id']
        var activated = content.activated
        LightStore.dispatch('toggleSensor', {sensorId, activated})
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
