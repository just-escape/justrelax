import Vue from 'vue'
import Vuex from 'vuex'

import publishSubscribeService from '@/store/publishSubscribeService.js'

Vue.use(Vuex)

let store = new Vuex.Store({
  state: {
    secretAnswers: [
      'biere',
      'beer',
      'bière',
    ],
    lastPressedCharacter: '',
    pressSignal: false,
    backspaceSignal: false,
    crSignal: false,
    displayPasswordWindow: false,
    displayPasswordRecoveryWindow: false,
    displayAlarmWindow: false,
    displayDangerWindow: false,
    showUI: false,
    success: false,
    overlayVideos: {
      ms_pepper_mad: {
        fr: require('@/assets/videos/ms_pepper_what_fr.mp4'),
        en: require('@/assets/videos/ms_pepper_what_en.mp4'),
      },
    },
    currentOverlayVideo: null,
    playingMarmitronAnimation: null,
    meals: [
      {
        id: "potjevleesch",
        n: 1,
        label: "Potjevleesch",
        labelPlural: "Potjevleesch",
        price: 10,
        baseMargin: 5.13,
        marginQualitySensitivity: -0.0086,
        quality: 40,
        cyclesQualitySensitivity: 1237,
        baseCycles: 3569125,
        verificationStatus: 'checking',
      },
      {
        n: 2,
        id: "salade_flamande",
        label: "Salade Flamande",
        labelPlural: "Salades Flamandes",
        price: 11,
        baseMargin: 4.54,
        marginQualitySensitivity: -0.0072,
        quality: 30,
        cyclesQualitySensitivity: 2461,
        baseCycles: 4569125,
        verificationStatus: null,
      },
      {
        id: "cambraisienne",
        n: 3,
        label: "Cambraisienne",
        labelPlural: "Cambraisiennes",
        price: 12,
        baseMargin: 6.79,
        marginQualitySensitivity: -0.0096,
        quality: 70,
        cyclesQualitySensitivity: 758,
        baseCycles: 1569125,
        verificationStatus: 'ok',
      },
      {
        id: "gaufresque",
        n: 4,
        label: "Gaufresque",
        labelPlural: "Gaufresques",
        price: 4,
        baseMargin: 2.17,
        marginQualitySensitivity: -0.0042,
        quality: 55,
        cyclesQualitySensitivity: 1894,
        baseCycles: 2989125,
        verificationStatus: 'ko',
      },
    ],
    availabilityLoading: false,
  },
  mutations: {
    checkAvailability(state, mealIndex) {
      state.availabilityLoading = true
      let event = {
        category: 'check_availability',
        id: state.meals[mealIndex].id,
      }
      publishSubscribeService.commit('publish', event)
    },
    notifyAvailability(state) {
      state.availabilityLoading = false
    },
    setQuality (state, {mealIndex, value}) {
      state.meals[mealIndex].quality = value
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
    showUI(state) {
      state.showUI = true
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
    displayAlarmWindow (state, display) {
      state.displayAlarmWindow = display
    },
    // eslint-disable-next-line
    passwordTry(state, password) {
      publishSubscribeService.commit('publish', {category: 'password_try', password: password})
    },
    // eslint-disable-next-line
    passwordRecoveryTry(state, secretAnswer) {
      publishSubscribeService.commit('publish', {category: 'password_recovery_try', secret_answer: secretAnswer})
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
    playAnimation(state, animationId) {
      state.playingMarmitronAnimation = animationId
    },
    finalAnimation (state) {
      state.playingMarmitronAnimation = 'liberation'
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
