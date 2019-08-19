import Vue from 'vue'
import Vuex from 'vuex'
import roomStore from '@/store/roomStore.js'

Vue.use(Vuex);

const justSockService = new Vuex.Store({
  state: {
    isConnected: false,
    messages: [],
    sentMessages: [],
    reconnectError: false,
  },
  mutations: {
    SOCKET_ONOPEN (state, event) {
      state.isConnected = true
      Vue.prototype.$socket = event.currentTarget
      Vue.prototype.$socket.send(JSON.stringify({"type": "IAM", "content": {"client_type": "$admin"}}))
    },
    SOCKET_ONCLOSE (state, event) {
      // eslint-disable-next-line
      console.error(state, event)
      state.isConnected = false
    },
    SOCKET_ONERROR (state, event) {
      // eslint-disable-next-line
      console.error(state, event)
    },
    SOCKET_ONMESSAGE (state, message) {
      state.messages.push(message.data)
      var event = JSON.parse(message.data)
      var channel = event.channel
      if (event.type == 'TIC') {
        var ticks = event.content
        roomStore.dispatch('beat', {channel, ticks})
      } else if (event.type == 'REC') {
        var record = event.content
        roomStore.dispatch('addRecord', {channel, record})
      } else if (event.type == 'CLR') {
        roomStore.dispatch('processReset', channel)
      }
    },
    SOCKET_RECONNECT (state, count) {
      // eslint-disable-next-line
      console.info(state, count)
    },
    SOCKET_RECONNECT_ERROR (state) {
      state.reconnectError = true
    },
    sendToGateway (state, message) {
      state.sentMessages.push(message)
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