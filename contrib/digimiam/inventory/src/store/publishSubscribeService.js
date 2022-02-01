import Vue from 'vue'
import Vuex from 'vuex'

import i18n from '@/locales.js'
import router from '@/router.js'
import sokobanStore from '@/store/sokobanStore.js'
import logStore from '@/store/logStore.js'
import progressionStore from '@/store/progressionStore.js'

Vue.use(Vuex)

const publishSubscribeService = new Vuex.Store({
  state: {
    name: "inventory",
    subscriptionChannels: [],
    publicationChannel: undefined,
  },
  mutations: {
    addSubscriptionChannel (state, subscriptionChannel) {
      state.subscriptionChannels.push(subscriptionChannel)
    },
    setPublicationChannel (state, publicationChannel) {
      state.publicationChannel = publicationChannel
    },
    SOCKET_ONOPEN (state, event) {
      Vue.prototype.$socket = event.currentTarget

      let query = JSON.parse(JSON.stringify(router.app.$route.query))

      if (query.name !== undefined) {
        state.name = query.name
      }

      for (let channel of state.subscriptionChannels) {
        let subscribeEvent = {
          action: "subscribe",
          channel: channel,
        }
        Vue.prototype.$socket.send(JSON.stringify(subscribeEvent))
      }

      sokobanStore.commit('publishSessionData')
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
      let event = message.event

      if (event.category === 'reset') {
        // Reload page
        router.go()
      } else if (event.category === 'set_locale') {
        let query = JSON.parse(JSON.stringify(router.app.$route.query))
        if (event.locale === 'fr') {
          if (i18n.locale != 'fr') {
            query.locale = 'fr'
            router.push({path: '/', query: query})
          }
          i18n.locale = 'fr'
        } else {
          if (i18n.locale != 'en') {
            query.locale = 'en'
            router.push({path: '/', query: query})
          }
          i18n.locale = 'en'
        }
      } else if (event.category === 'log') {
        let logMessage = event.message
        let level = event.level
        let useLocale = event.use_locale
        let withSound = event.with_sound === undefined ? true : event.with_sound
        logStore.commit('processLog', {logMessage, level, useLocale, withSound})
      } else if (event.category === 'set_difficulty') {
        sokobanStore.commit('setDifficulty', event.difficulty)
      } else if (event.category === 'control') {
        sokobanStore.commit('control', {name: event.name, pressed: event.pressed})
      } else if (event.category === 'queue_moves') {
        sokobanStore.commit('queueMoves', event.moves || [])
      } else if (event.category === 'display_danger_window') {
        progressionStore.commit('displayDangerWindow')
      } else if (event.category === 'display_black_screen') {
        let display = event.display ? true : false
        progressionStore.commit('displayBlackScreen', display)
      } else if (event.category === 'set_stocks_status') {
        progressionStore.commit('setIsStocksOk', event.status)
      } else if (event.category === 'request_node_session_data') {
        sokobanStore.commit('publishSessionData')
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
    publish (state, event) {
      event.from_ = state.name
      let json = JSON.stringify({action: "publish", channel: state.publicationChannel, event: event})
      Vue.prototype.$socket.send(json)
    },
  },
})

export default publishSubscribeService
