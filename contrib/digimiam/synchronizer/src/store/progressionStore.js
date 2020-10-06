import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

import justSockService from '@/store/justSockService.js'

let store = new Vuex.Store({
  state: {
    lightServiceSuccess: false,
    menuServiceSuccess: false,
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
    setLightServiceSuccess(state) {
      if (!state.lightServiceSuccess) {
        state.lightServiceSuccess = true
        justSockService.commit("sendEvent", {"category": "light_service_success"})

        if (state.menuServiceSuccess) {
          justSockService.commit("sendEvent", {"category": "services_synchronization_success"})
        }
      }
    },
    setMenuServiceSuccess(state) {
      if (!state.menuServiceSuccess) {
        state.menuServiceSuccess = true
        justSockService.commit("sendEvent", {"category": "menu_service_success"})

        if (state.lightServiceSuccess) {
          justSockService.commit("sendEvent", {"category": "services_synchronization_success"})
        }
      }
    },
  }
})

export default store
