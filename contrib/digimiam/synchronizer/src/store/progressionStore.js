import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

import publishSubscribeService from '@/store/publishSubscribeService.js'

let store = new Vuex.Store({
  state: {
    lightServiceSuccess: false,
    menuServiceSuccess: false,
    displayDangerWindow: false,
    overlayVideos: {
      glitching: {
        fr: require('@/assets/videos/ads_glitch.webm'),
        en: require('@/assets/videos/ads_glitch.webm'),
      },
      ads_loop: {
        fr: require('@/assets/videos/ads_loop.webm'),
        en: require('@/assets/videos/ads_loop.webm'),
      },
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
        publishSubscribeService.commit("publish", {"category": "light_service_success"})

        if (state.menuServiceSuccess) {
          publishSubscribeService.commit("publish", {"category": "services_synchronization_success"})
        }
      }
    },
    setMenuServiceSuccess(state) {
      if (!state.menuServiceSuccess) {
        state.menuServiceSuccess = true
        publishSubscribeService.commit("publish", {"category": "menu_service_success"})

        if (state.lightServiceSuccess) {
          publishSubscribeService.commit("publish", {"category": "services_synchronization_success"})
        }
      }
    },
  }
})

export default store
