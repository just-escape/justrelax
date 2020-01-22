import Vue from 'vue'
import Vuex from 'vuex'
import roomStore from '@/store/roomStore.js'
import notificationStore from '@/store/notificationStore.js'

Vue.use(Vuex);

const justSockService = new Vuex.Store({
  mutations: {
    SOCKET_ONOPEN (state, event) {
      Vue.prototype.$socket = event.currentTarget
      let iamMessage = {
        message_type: "IAM",
        client_type: "admin"
      }
      Vue.prototype.$socket.send(JSON.stringify(iamMessage))
    },
    // eslint-disable-next-line
    SOCKET_ONCLOSE (state, event) {
      notificationStore.dispatch('pushError', 'Websocket connection lost')
    },
    // eslint-disable-next-line
    SOCKET_ONERROR (state, event) {
      notificationStore.dispatch('pushError', 'Websocket error')
    },
    SOCKET_ONMESSAGE (state, rawMessage) {
      let message = JSON.parse(rawMessage.data)
      let roomId = message.room_id
      if (message.message_type == 'TIC') {
        let ticks = message.ticks
        roomStore.dispatch('beat', {roomId, ticks})
      } else if (message.message_type == 'NOTIFICATION') {
        let type = message.notification_type
        let notificationMessage = message.notification_message
        notificationStore.commit('pushNotification', {type: type, message: notificationMessage})
      } else if (message.message_type == 'REC') {
        let recordId = message.record_id
        let recordTicks = message.ticks
        let recordLabel = message.label
        roomStore.dispatch('addRecord', {roomId, recordId, recordTicks, recordLabel})
      } else if (message.message_type == 'RESET') {
        roomStore.commit('processReset', roomId)
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
    sendMessage (state, message) {
      let jsonMessage = JSON.stringify(message)
      Vue.prototype.$socket.send(jsonMessage)
    },
  },
})

export default justSockService