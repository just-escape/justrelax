import Vue from 'vue'
import Vuex from 'vuex'

import orderStore from '@/store/orderStore.js'
import publishSubcribeService from '@/store/publishSubscribeService.js'

Vue.use(Vuex)

let store = new Vuex.Store({
  state: {
    round: 0,
    showMarmitron: true,
    showDocumentation: false,
    isOrderOnHold: false,
    isRestaurantClosed: false,
    displayDangerWindow: false,
    displayBlackScreen: false,
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
    currentInstructionStrings: [''],
    currentInstructionStringsUseLocale: true,
    currentInstructionLoop: false,
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
    setIsOrderOnHold (state, value) {
      state.isOrderOnHold = value
    },
    setRestaurantStatus (state, closed) {
      state.isRestaurantClosed = closed
      orderStore.commit('resetOrder')
    },
    fireHelpAnimation (state) {
      state.fireHelpAnimation = true
    },
    playOverlayVideo(state, videoId) {
      if (state.overlayVideos[videoId]) {
        state.currentOverlayVideo = videoId
      }

      // Not clean :|
      // But it ensures a perfect continuity between Marmitron's idle animation and the help animation
      if (videoId === 'ms_pepper_says_thanks') {
        let ms_pepper_says_thanks_duration = 16960
        let idle_duration = 8000
        let delay_between_animations = 2400
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
        publishSubcribeService.commit('publish', {category: 'ms_pepper_has_told_to_go_in_stock'})
      } else if (state.currentOverlayVideo === "ms_pepper_says_thanks") {
        publishSubcribeService.commit('publish', {category: 'ms_pepper_has_said_thanks'})
      }

      state.currentOverlayVideo = null
    },
    displayDangerWindow(state) {
      state.displayDangerWindow = true
    },
    highlightUnplugInstruction(state, highlight) {
      state.highlightUnplugInstruction = highlight
    },
    setDocumentationCurrentInstruction(state, {message, useLocale, loop}) {
      state.currentInstructionStrings = message
      state.currentInstructionStringsUseLocale = useLocale
      state.currentInstructionLoop = loop
    },
    displayBlackScreen(state, value) {
      state.displayBlackScreen = value
    },
  }
})

export default store
