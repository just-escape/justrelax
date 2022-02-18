import Vue from 'vue'
import Vuex from 'vuex'

import i18n from '@/locales.js'
import router from '@/router.js'

import orderStore from '@/store/orderStore.js'
import progressionStore from '@/store/progressionStore.js'

Vue.use(Vuex)

const publishSubscribeService = new Vuex.Store({
  state: {
    name: "orders",
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
      } else if (event.category === 'play_overlay_video') {
        progressionStore.commit('playOverlayVideo', event.video_id)
      } else if (event.category === 'stop_overlay_video') {
        progressionStore.commit('stopOverlayVideo')
      } else if (event.category === 'set_ventilation_panel_round') {
        progressionStore.commit('setRound', event.round)
      } else if (event.category === 'set_documentation_visibility') {
        progressionStore.commit('setDocumentationVisibility', event.show)
      } else if (event.category === 'set_marmitron_visibility') {
        progressionStore.commit('setMarmitronVisibility', event.show)
      } else if (event.category === 'set_restaurant_status') {
        progressionStore.commit('setRestaurantStatus', event.closed)
      } else if (event.category === 'display_danger_window') {
        progressionStore.commit('displayDangerWindow')
      } else if (event.category === 'set_display_empty_cart_help') {
        orderStore.commit('setDisplayEmptyCartHelp', event.value)
      } else if (event.category === 'set_credits') {
        orderStore.commit('setCredits', event.value)
      } else if (event.category === 'set_documentation_current_instruction') {
        let instructionMessage
        let loop
        if (!Array.isArray(event.message)) {
          instructionMessage = [event.message]
          loop = false
        } else {
          instructionMessage = event.message
          loop = true
        }
        progressionStore.commit('setDocumentationCurrentInstruction', {message: instructionMessage, useLocale: event.use_locale || false, loop: event.loop || loop})
      } else if (event.category === 'set_display_resume_order_notification') {
        orderStore.commit('setDisplayResumeOrderNotification', event.value)
      } else if (event.category === 'set_display_order_recap_notification') {
        orderStore.commit('setDisplayOrderRecapNotification', event.value)
      } else if (event.category === 'reset_order') {
        orderStore.commit('resetOrder')
      } else if (event.category === 'set_display_processing_order_notification') {
        orderStore.commit('setDisplayProcessingOrderNotification', event.value)
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
    publish (state, event) {
      event.from_ = state.name
      let json = JSON.stringify({action: "publish", channel: state.publicationChannel, event: event})
      Vue.prototype.$socket.send(json)
    },
  },
})

export default publishSubscribeService
