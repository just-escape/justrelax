import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

import lightLogStore from '@/store/lightLogStore.js'
import menuLogStore from '@/store/menuLogStore.js'
import publishSubscribeService from '@/store/publishSubscribeService.js'

let store = new Vuex.Store({
  state: {
    lightServiceSuccess: false,
    menuServiceSuccess: false,
    displayDangerWindow: false,
    displayBlackScreen: false,
    overlayVideos: {
      glitching: {
        fr: require('@/assets/videos/ads_glitch.webm'),
        en: require('@/assets/videos/ads_glitch.webm'),
        loop: true,
      },
      ads_loop: {
        fr: require('@/assets/videos/waffresco_ad_loop_fr.mp4'),
        en: require('@/assets/videos/waffresco_ad_loop_en.mp4'),
        loop: true,
      },
    },
    currentOverlayVideo: null,
    msPepperOverlayVideos: {
      ms_pepper_stock: {
        media: require('@/assets/videos/ms_pepper_stock_muted.mp4'),
        loop: false,
      },
      ms_pepper_says_thanks: {
        media: require('@/assets/videos/ms_pepper_says_thanks_muted.mp4'),
        loop: false,
      },
    },
    currentMsPepperOverlayVideo: null,
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
    playMsPepperOverlayVideo(state, videoId) {
      if (state.msPepperOverlayVideos[videoId]) {
        state.currentMsPepperOverlayVideo = videoId
      }
    },
    stopMsPepperOverlayVideo(state) {
      state.currentMsPepperOverlayVideo = null
    },
    setLightServiceSuccess(state) {
      if (!state.lightServiceSuccess) {
        state.lightServiceSuccess = true
        publishSubscribeService.commit("publish", {"category": "light_service_success"})
        lightLogStore.commit("processLog", {logMessage: "light_sync_complete", level: "info", useLocale: true, withSound: false})

        if (state.menuServiceSuccess) {
          publishSubscribeService.commit("publish", {"category": "services_synchronization_success"})
        }
      }
    },
    setMenuServiceSuccess(state) {
      if (!state.menuServiceSuccess) {
        state.menuServiceSuccess = true
        publishSubscribeService.commit("publish", {"category": "menu_service_success"})
        menuLogStore.commit("processLog", {logMessage: "menu_reconfig_complete", level: "info", useLocale: true, withSound: false})

        if (state.lightServiceSuccess) {
          publishSubscribeService.commit("publish", {"category": "services_synchronization_success"})
        }
      }
    },
    displayBlackScreen(state, value) {
      state.displayBlackScreen = value
    },
  }
})

export default store
