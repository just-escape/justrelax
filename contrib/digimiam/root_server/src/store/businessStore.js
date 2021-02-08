import Vue from 'vue'
import Vuex from 'vuex'

import publishSubscribeService from '@/store/publishSubscribeService.js'

Vue.use(Vuex)

let store = new Vuex.Store({
  state: {
    secretAnswers: [
      'biere'
    ],
    lastPressedCharacter: '',
    pressSignal: false,
    backspaceSignal: false,
    crSignal: false,
    displayPasswordWindow: false,
    displayPasswordRecoveryWindow: false,
    displayDangerWindow: false,
    success: false,
    overlayVideos: {
      ms_pepper_mad: {
        fr: require('@/assets/videos/ms_pepper_what_fr.mp4'),
        en: require('@/assets/videos/ms_pepper_what_en.mp4'),
      },
    },
    currentOverlayVideo: null,
    playingMarmitronAnimation: null,
  },
  mutations: {
    playMarmitronAnimation (state, animationId) {
      state.playingMarmitronAnimation = animationId
    },
    press (state, character) {
      if (!state.success) {
        state.lastPressedCharacter = character
        state.pressSignal = !state.pressSignal
      }
    },
    backspace (state) {
      if (!state.success) {
        state.backspaceSignal = !state.backspaceSignal
      }
    },
    cr (state) {
      if (!state.success) {
        state.crSignal = !state.crSignal
      }
    },
    displayPasswordWindow (state) {
      state.displayPasswordWindow = true
    },
    hidePasswordWindow (state) {
      state.displayPasswordWindow = false
    },
    displayPasswordRecoveryWindow (state) {
      state.displayPasswordRecoveryWindow = true
    },
    hidePasswordRecoveryWindow (state) {
      state.displayPasswordRecoveryWindow = false
    },
    displayDangerWindow (state) {
      state.displayDangerWindow = true
    },
    success (state) {
      if (!state.success) {
        state.success = true
        let event = {
          category: 'success',
        }
        publishSubscribeService.commit('publish', event)
      }
    },
    finalAnimation () {
      store.commit('playMarmitronAnimation', 'liberation')
      setTimeout(store.commit, 400, 'hidePasswordRecoveryWindow')
      setTimeout(store.commit, 500, 'hidePasswordWindow')
      setTimeout(store.commit, 12000, 'playOverlayVideo', 'ms_pepper_mad')
    },
    playOverlayVideo(state, videoId) {
      if (state.overlayVideos[videoId] !== undefined) {
        state.currentOverlayVideo = videoId
      }
    },
    onOverlayVideoEnd(state) {
      // Not clean :|
      if (state.currentOverlayVideo === "ms_pepper_mad") {
        let event = {
          category: 'ms_pepper_mad_end',
        }
        publishSubscribeService.commit('publish', event)
      }

      state.currentOverlayVideo = null
    },
  }
})

export default store
