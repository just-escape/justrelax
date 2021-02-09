import Vue from 'vue'
import Vuex from 'vuex'
import roomStore from '@/store/roomStore.js'
import notificationStore from '@/store/notificationStore.js'

Vue.use(Vuex)

const publishSubscribeService = new Vuex.Store({
  state: {
    name: "webmin",
    subscriptions: [],
  },
  mutations: {
    SOCKET_ONOPEN (state, event) {
      Vue.prototype.$socket = event.currentTarget
      for (let channel in state.subscriptions) {
        let subscribeEvent = {
          action: "subscribe",
          channel: channel,
        }
        Vue.prototype.$socket.send(JSON.stringify(subscribeEvent))
      }
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

      // Listening on the error channel is hardcoded
      if (message.channel === 'error') {
        let logMessage = message.event.hostname + ': ' + message.event.log
        notificationStore.commit('pushNotification', {type: 'error', message: logMessage})
      }

      roomStore.commit('processEvent', {channel: message.channel, event: message.event})
    },
    // eslint-disable-next-line
    SOCKET_RECONNECT (state, count) {
      notificationStore.dispatch('pushError', 'Attempting reconnection to websocket (' + count + ')')
    },
    // eslint-disable-next-line
    SOCKET_RECONNECT_ERROR (state) {
      notificationStore.dispatch('pushError', 'Websocket reconnection error')
    },
    subscribe (state, channel) {
      if (!state.subscriptions.includes(channel)) {
        state.subscriptions.push(channel)
        let subscribeEvent = {
          action: "subscribe",
          channel: channel,
        }
        Vue.prototype.$socket.send(JSON.stringify(subscribeEvent))
      }
    },
    // eslint-disable-next-line
    publish (state, {channel, event}) {
      event.from = state.name
      let json = JSON.stringify({action: "publish", channel: channel, event: event})
      Vue.prototype.$socket.send(json)
    },
  },
})

export default publishSubscribeService