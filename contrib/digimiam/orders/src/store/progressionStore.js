import Vue from 'vue'
import Vuex from 'vuex'

import orderStore from '@/store/orderStore.js'

Vue.use(Vuex)

let store = new Vuex.Store({
  state: {
    round: 0,
    showDocumentation: false,
    isRestaurantClosed: false,
    displayDangerWindow: false,
    runMsPepperPantryAfterNotificationAcknowledgement: false,
    overlayVideos: {
      glitching: {
        fr: require('@/assets/glitch.mp4'),
        en: require('@/assets/glitch.mp4'),
        loop: true,
      },
      glitching_less: {
        fr: require('@/assets/glitch_less.mp4'),
        en: require('@/assets/glitch_less.mp4'),
        loop: true,
      },
      ms_pepper_pantry: {
        fr: require('@/assets/mme_poivre_stock.mp4'),
        en: require('@/assets/ms_pepper_pantry.mp4'),
        loop: false,
      },
      ms_pepper_thanks: {
        fr: require('@/assets/mme_poivre_merci.mp4'),
        en: require('@/assets/ms_pepper_says_thanks.mp4'),
        loop: false,
      },
    },
    currentOverlayVideo: null,
  },
  mutations: {
    setRound (state, round) {
      state.round = round
    },
    setDocumentationVisibility (state, show) {
      state.showDocumentation = show
    },
    setRestaurantStatus (state, closed) {
      state.isRestaurantClosed = closed
      orderStore.commit('resetOrder')
    },
    runMsPepperPantryAfterNotificationAcknowledgement (state) {
      state.runMsPepperPantryAfterNotificationAcknowledgement = true
    },
    playOverlayVideo(state, videoId) {
      if (state.overlayVideos[videoId]) {
        state.currentOverlayVideo = videoId
      }
    },
    stopOverlayVideo(state) {
      state.currentOverlayVideo = null
    },
    onOverlayVideoEnd(state) {
      // Not clean :|
      if (state.currentOverlayVideo === "ms_pepper_pantry") {
        state.runMsPepperPantryAfterNotificationAcknowledgement = false
        setTimeout(store.commit, 800, 'setDocumentationVisibility', true)
      }

      state.currentOverlayVideo = null
    },
    displayDangerWindow(state) {
      state.displayDangerWindow = true
    },
  }
})

export default store
