import Vue from 'vue'
import Vuex from 'vuex'
import store from '@/store/store.js'

Vue.use(Vuex);

const justSockService = new Vuex.Store({
  mutations: {
    SOCKET_ONOPEN (state, event) {
      Vue.prototype.$socket = event.currentTarget
      Vue.prototype.$socket.send(
        JSON.stringify(
          {
            "type": "IAM",
            "content": {
              "client_type": "$node",
              "channel": "digimiam1",
              "name": "inventory",
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
      if (event.type == 'MSG') {
        var content = event.content
        store.commit('processEvent', content)
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
