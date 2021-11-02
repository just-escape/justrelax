import Vue from 'vue'
import Vuex from 'vuex'

import i18n from '@/locales.js'
import router from '@/router.js'

import businessStore from '@/store/businessStore.js'

Vue.use(Vuex)

const publishSubscribeService = new Vuex.Store({
  state: {
    name: "root_server",
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
    // eslint-disable-next-line
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
        if (event.locale == 'fr') {
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
      } else if (event.category === 'show_ui') {
        businessStore.commit('showUI')
      } else if (event.category === 'display_password_window') {
        businessStore.commit('displayPasswordWindow')
      } else if (event.category === 'play_animation') {
        businessStore.commit('playAnimation', event.animation)
      } else if (event.category === 'final_animation') {
        businessStore.commit('finalAnimation')
      } else if (event.category === 'display_danger_window') {
        businessStore.commit('displayDangerWindow')
      } else if (event.category === 'display_alarm_window') {
        businessStore.commit('displayAlarmWindow', event.display)
      } else if (event.category === 'availability') {
        businessStore.commit('notifyAvailability', {mealId: event.id, missingIngredients: event.missing_ingredients})
      } else if (event.category === "force_success") {
        businessStore.commit('success')
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
      event.from = state.name
      let json = JSON.stringify({action: "publish", channel: state.publicationChannel, event: event})
      Vue.prototype.$socket.send(json)
    },
  },
})

export default publishSubscribeService
