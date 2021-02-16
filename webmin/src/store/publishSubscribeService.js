import Vue from 'vue'
import Vuex from 'vuex'
import roomStore from '@/store/roomStore.js'
import notificationStore from '@/store/notificationStore.js'

Vue.use(Vuex)

const publishSubscribeService = new Vuex.Store({
  state: {
    isWebSocketOpened: false,
    name: "webmin",
    subscriptions: [],
    onConnectionPublications: [],
  },
  mutations: {
    SOCKET_ONOPEN (state, event) {
      state.isWebSocketOpened = true

      Vue.prototype.$socket = event.currentTarget
      for (let channel of state.subscriptions) {
        let subscribeEvent = {
          action: "subscribe",
          channel: channel,
        }
        Vue.prototype.$socket.send(JSON.stringify(subscribeEvent))
      }

      for (let connectionPublication of state.onConnectionPublications) {
        publishSubscribeService.commit('publish', {channel: connectionPublication.channel, event: connectionPublication.event})
      }
    },
    // eslint-disable-next-line
    SOCKET_ONCLOSE (state, event) {
      state.isWebSocketOpened = false
      notificationStore.dispatch('pushError', 'Web socket connection lost')
    },
    // eslint-disable-next-line
    SOCKET_ONERROR (state, event) {
      state.isWebSocketOpened = false
      notificationStore.dispatch('pushError', 'Web socket error')
    },
    SOCKET_ONMESSAGE (state, rawMessage) {
      let message = JSON.parse(rawMessage.data)

      // Listening on the error channel is hardcoded
      if (message.channel === 'error') {
        let logMessage = message.event.hostname + ': ' + message.event.log
        notificationStore.commit('pushNotification', {type: 'error', message: logMessage})
      }

      roomStore.commit('processEvent', {channel: message.channel, event: message.event})
    },
    // eslint-disable-next-line
    SOCKET_RECONNECT (state, count) {
      notificationStore.dispatch('pushError', 'Attempting reconnection to web socket (' + count + ')')
    },
    // eslint-disable-next-line
    SOCKET_RECONNECT_ERROR (state) {
      notificationStore.dispatch('pushError', 'Web socket reconnection error')
    },
    addOnConnectionPublication(state, {channel, event}) {
      state.onConnectionPublications.push({channel: channel, event: event})

      if (state.isWebSocketOpened) {
        // If it's already opened we should send it directly or we will never see it
        publishSubscribeService.commit('publish', {channel: channel, event: event})
      }
    },
    subscribe (state, channel) {
      if (!state.subscriptions.includes(channel)) {
        state.subscriptions.push(channel)

        if (state.isWebSocketOpened) {
          // If the web socket is not opened, the subscription event will be sent in SOCKET_ONOPEN
          let subscribeEvent = {
            action: "subscribe",
            channel: channel,
          }
          Vue.prototype.$socket.send(JSON.stringify(subscribeEvent))
        }
      }
    },
    // eslint-disable-next-line
    publish (state, {channel, event}) {
      if (state.isWebSocketOpened) {
        event.from = state.name
        let json = JSON.stringify({action: "publish", channel: channel, event: event})
        Vue.prototype.$socket.send(json)
      } else {
        notificationStore.dispatch('pushError', 'Web socket connection is not established: event has not been sent')
      }
    },
  },
})

export default publishSubscribeService