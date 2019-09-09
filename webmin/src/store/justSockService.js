import Vue from 'vue'
import Vuex from 'vuex'
import roomStore from '@/store/roomStore.js'
import notificationStore from '@/store/notificationStore.js'

Vue.use(Vuex);

const justSockService = new Vuex.Store({
  mutations: {
    SOCKET_ONOPEN (state, event) {
      Vue.prototype.$socket = event.currentTarget
      Vue.prototype.$socket.send(JSON.stringify({"type": "IAM", "content": {"client_type": "$admin"}}))
    },
    // eslint-disable-next-line
    SOCKET_ONCLOSE (state, event) {
      notificationStore.dispatch('pushError', 'Websocket connection lost')
    },
    // eslint-disable-next-line
    SOCKET_ONERROR (state, event) {
      notificationStore.dispatch('pushError', 'Websocket error')
    },
    SOCKET_ONMESSAGE (state, message) {
      var event = JSON.parse(message.data)
      var roomId = event.room_id
      if (event.type == 'TIC') {
        var ticks = event.content
        roomStore.dispatch('beat', {roomId, ticks})
      } else if (event.type == 'REC') {
        var record = event.content
        roomStore.dispatch('addRecord', {roomId, record})
      } else if (event.type == 'CLR') {
        roomStore.dispatch('processReset', roomId)
      }
    },
    // eslint-disable-next-line
    SOCKET_RECONNECT (state, count) {
      notificationStore.dispatch('pushError', 'Attempting reconnection to websocket (' + count + ')')
    },
    // eslint-disable-next-line
    SOCKET_RECONNECT_ERROR (state) {
      notificationStore.dispatch('pushError', 'Websocket reconnection error')
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