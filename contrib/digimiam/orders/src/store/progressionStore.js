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
    runMsPepperStockAfterNotificationAcknowledgement: false,
    overlayVideos: {
      glitching: {
        fr: require('@/assets/videos/orders_glitch.webm'),
        en: require('@/assets/videos/orders_glitch.webm'),
        loop: true,
      },
      glitching_less: {
        fr: require('@/assets/videos/orders_glitch_bios.webm'),
        en: require('@/assets/videos/orders_glitch_bios.webm'),
        loop: true,
      },
      ms_pepper_stock: {
        fr: require('@/assets/videos/ms_pepper_stock_fr.mp4'),
        en: require('@/assets/videos/ms_pepper_stock_en.mp4'),
        loop: false,
      },
      ms_pepper_says_thanks: {
        fr: require('@/assets/videos/ms_pepper_says_thanks_fr.mp4'),
        en: require('@/assets/videos/ms_pepper_says_thanks_en.mp4'),
        loop: false,
      },
    },
    currentOverlayVideo: null,
    fireHelpAnimation: false,
    highlightUnplugInstruction: false,
  },
  mutations: {
    setRound (state, round) {
      state.round = round
    },
    setDocumentationVisibility (state, show) {
      state.showDocumentation = show
    },
    setMarmitronVisibility (state, show) {
      state.showMarmitron = show
    },
    setRestaurantStatus (state, closed) {
      state.isRestaurantClosed = closed
      orderStore.commit('resetOrder')
    },
    runMsPepperStockAfterNotificationAcknowledgement (state) {
      state.runMsPepperStockAfterNotificationAcknowledgement = true
    },
    fireHelpAnimation (state) {
      state.fireHelpAnimation = true
    },
    playOverlayVideo(state, videoId) {
      if (state.overlayVideos[videoId]) {
        state.currentOverlayVideo = videoId
      }

      // Not clean :|
      if (videoId === 'ms_pepper_says_thanks') {
        let ms_pepper_says_thanks_duration = 16960
        let idle_duration = 8000
        let delay_between_animations = 5000
        setTimeout(
          store.commit,
          ms_pepper_says_thanks_duration - (idle_duration - delay_between_animations),
          'fireHelpAnimation')
      }
    },
    stopOverlayVideo(state) {
      state.currentOverlayVideo = null
    },
    onOverlayVideoEnd(state) {
      // Not clean :|
      if (state.currentOverlayVideo === "ms_pepper_stock") {
        state.runMsPepperStockAfterNotificationAcknowledgement = false
        setTimeout(store.commit, 800, 'setDocumentationVisibility', true)
      }

      state.currentOverlayVideo = null
    },
    displayDangerWindow(state) {
      state.displayDangerWindow = true
    },
    highlightUnplugInstruction(state, highlight) {
      state.highlightUnplugInstruction = highlight
    },
  }
})

export default store
