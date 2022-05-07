import Vue from 'vue'
import Vuex from 'vuex'

import i18n from '@/locales.js'
import router from '@/router.js'

import lightStore from '@/store/lightStore.js'
import menuLogStore from '@/store/menuLogStore.js'
import lightLogStore from '@/store/lightLogStore.js'
import difficultyStore from '@/store/difficultyStore.js'
import menuStore from '@/store/menuStore.js'
import progressionStore from '@/store/progressionStore.js'

Vue.use(Vuex)

const publishSubscribeService = new Vuex.Store({
  state: {
    isWebSocketOpened: false,
    name: "synchronizer",
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
      state.isWebSocketOpened = true

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

      menuStore.commit('publishSessionData')
      lightStore.commit('publishSessionData')
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
      } else if (event.category === 'set_difficulty') {
        difficultyStore.commit('setDifficulty', event.difficulty)
      } else if (event.category === 'set_light_difficulty') {
        lightStore.commit('setDifficulty', event.difficulty)
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
      } else if (event.category === 'menu_log') {
        let logMessage = event.message
        let level = event.level
        let useLocale = event.use_locale
        let withSound = event.with_sound === undefined ? true : event.with_sound
        menuLogStore.commit('processLog', {logMessage, level, useLocale, withSound})
      } else if (event.category === 'light_log') {
        let logMessage = event.message
        let level = event.level
        let useLocale = event.use_locale
        let withSound = event.with_sound === undefined ? true : event.with_sound
        lightLogStore.commit('processLog', {logMessage, level, useLocale, withSound})
      } else if (event.category === 'set_menu_cursor_position') {
        menuStore.commit('setMenuCursorPosition', event.position)
      } else if (event.category === 'force_menu_success') {
        menuStore.commit('forceSuccess')
      } else if (event.category === 'force_light_success') {
        progressionStore.commit('setLightServiceSuccess')
      } else if (event.category === 'load_cell') {
        let color = event.color
        let id = event.id
        let activated = event.activated
        lightStore.dispatch('toggleColor', {color, id, activated})
      } else if (event.category === 'restaurant_in_manual_mode') {
        lightStore.commit('setRestaurantInManualMode')
        menuStore.commit('pushMenuEntry', {itemIndex: 3, onManualMode: true, getters: menuStore.getters})
        menuStore.commit('pushMenuEntry', {itemIndex: 2, onManualMode: true, getters: menuStore.getters})
        menuStore.commit('pushMenuEntry', {itemIndex: 1, onManualMode: true, getters: menuStore.getters})
        menuStore.commit('pushMenuEntry', {itemIndex: 0, onManualMode: true, getters: menuStore.getters})
      } else if (event.category === 'display_danger_window') {
        progressionStore.commit('displayDangerWindow')
      } else if (event.category === 'play_overlay_video') {
        progressionStore.commit('playOverlayVideo', event.video_id)
      } else if (event.category === 'stop_overlay_video') {
        progressionStore.commit('stopOverlayVideo')
      } else if (event.category === 'play_ms_pepper_overlay_video') {
        progressionStore.commit('playMsPepperOverlayVideo', event.video_id)
      } else if (event.category === 'stop_ms_pepper_overlay_video') {
        progressionStore.commit('stopMsPepperOverlayVideo')
      } else if (event.category === 'set_auto_validate_dishes') {
        menuStore.commit('setAutoValidateDishes', event.value)
      } else if (event.category === 'display_price') {
        menuStore.commit('setDisplayPrice', event.display)
      } else if (event.category === 'set_color_disabled') {
        lightStore.commit('setColorDisabled', {color: event.color, isDisabled: event.is_disabled})
      } else if (event.category === 'request_node_session_data') {
        publishSubscribeService.commit('publish',
          {
            'category': 'set_session_data',
            'key': 'synchronizer_disabled_colors',
            'data': lightStore.state.disabledColors,
          }
        )
        menuStore.commit('publishSessionData')
        lightStore.commit('publishSessionData')
      } else if (event.category === 'set_price_matters') {
        menuStore.commit('setPriceMatters', event.value)
      } else if (event.category === 'set_display_menu_explicit_instruction') {
        menuStore.commit('setDisplayMenuExplicitInstruction', event.value)
      } else if (event.category === 'set_display_light_explicit_instruction') {
        lightStore.commit('setDisplayLightExplicitInstruction', event.value)
      } else if (event.category === 'set_strict_loading_mode') {
        lightStore.commit('setStrictLoadingMode', event.value)
      } else if (event.category === 'set_display_holographic_update_on_change') {
        menuStore.commit('setDisplayHolographicUpdateOnChange', event.value)
      } else if (event.category === 'display_black_screen') {
        let display = event.display ? true : false
        progressionStore.commit('displayBlackScreen', display)
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
