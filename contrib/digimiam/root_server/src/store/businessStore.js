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
        n: 1,
        id: "salade_flamande",
        label: "Salade Flamande",
        labelPlural: "Salades Flamandes",
        price: 10,
        baseMargin: 3,
        marginQualitySensitivity: 0.1,
        quality: 50,
        cyclesQualitySensitivity: 1,
        baseCycles: 1000,
        verificationStatus: null,
      },
      {
        id: "potjevleesch",
        n: 2,
        label: "Potjevleesch",
        labelPlural: "Potjevleesch",
        price: 11,
        baseMargin: 3,
        marginQualitySensitivity: 0.1,
        quality: 50,
        cyclesQualitySensitivity: 1,
        baseCycles: 1000,
        verificationStatus: 'checking',
      },
      {
        id: "cambraisienne",
        n: 3,
        label: "Cambraisienne",
        labelPlural: "Cambraisiennes",
        price: 12,
        baseMargin: 3,
        marginQualitySensitivity: 0.1,
        quality: 50,
        cyclesQualitySensitivity: 1,
        baseCycles: 1000000,
        verificationStatus: 'ok',
      },
      {
        id: "gaufresque",
        n: 4,
        label: "Gaufresque",
        labelPlural: "Gaufresques",
        price: 4,
        baseMargin: 3,
        marginQualitySensitivity: 0.1,
        quality: 50,
        cyclesQualitySensitivity: 1,
        baseCycles: 1000000,
        verificationStatus: 'ko',
      },
    ],
    availabilityNotificationSignal: false,
    availabilityNotificationId: undefined,
    availabilityNotificationMissingIngredients: false,
  },
  mutations: {
    checkAvailability(state, mealIndex) {
      let event = {
        category: 'check_availability',
        id: state.meals[mealIndex].id,
      }
      publishSubscribeService.commit('publish', event)
    },
    notifyAvailability(state, {mealId, missingIngredients}) {
      state.availabilityNotificationSignal = !state.availabilityNotificationSignal
      state.availabilityNotificationId = mealId
      state.availabilityNotificationMissingIngredients = missingIngredients
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
      state.playingMarmitronAnimation = 'final'
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
