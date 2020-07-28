import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

let store = new Vuex.Store({
  state: {
    displayDangerWindow: false,
    overlayVideos: {
      glitching: require('@/assets/videos/ads_glitch.webm'),
    },
    currentOverlayVideo: null,
  },
  mutations: {
    displayDangerWindow(state) {
      state.displayDangerWindow = true
    },
    playOverlayVideo(state, videoId) {
      if (state.overlayVideos[videoId]) {
        state.currentOverlayVideo = videoId
      }
    },
    stopOverlayVideo(state) {
      state.currentOverlayVideo = null
    },
  }
})

export default store
