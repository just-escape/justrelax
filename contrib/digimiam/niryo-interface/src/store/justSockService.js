import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

const justSockService = new Vuex.Store({
  mutations: {
    SOCKET_ONOPEN (state, event) {
      Vue.prototype.$socket = event.currentTarget
      let iamMessage = {
        message_type: "IAM",
        client_type: "node",
        channel: "digimiam1",
        name: "controler",
      }
      Vue.prototype.$socket.send(JSON.stringify(iamMessage))
    },
    // eslint-disable-next-line
    SOCKET_ONCLOSE (state, event) {
      console.error(event)
    },
    // eslint-disable-next-line
    SOCKET_ONERROR (state, event) {
      console.error(event)
    },
    SOCKET_ONMESSAGE (state, rawMessage) {
      let message = JSON.parse(rawMessage.data)
      if (message.message_type != 'EVENT') {
        return
      }
    },
    // eslint-disable-next-line
    SOCKET_RECONNECT (state, count) {
      console.info(count)
    },
    // eslint-disable-next-line
    SOCKET_RECONNECT_ERROR (state) {
      console.error('Websocket reconnection error')
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
  }
})

export default justSockService