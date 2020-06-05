import Vue from 'vue'
import Vuex from 'vuex'

import orderStore from '@/store/orderStore.js'

Vue.use(Vuex)

let store = new Vuex.Store({
  state: {
    round: 0,
    showDocumentation: false,
    isRestaurantClosed: false,
    runCutsceneAfterNotificationAcknowledgement: false,
    cutscenes: {
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
    currentCutscene: 'glitching',
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
    runCutsceneAfterNotificationAcknowledgement (state) {
      state.runCutsceneAfterNotificationAcknowledgement = true
    },
    playCutscene(state, cutsceneId) {
      if (state.cutscenes[cutsceneId]) {
        state.currentCutscene = cutsceneId
      }
    },
    stopCutscene(state) {
      state.currentCutscene = null
    },
    onCutsceneEnd(state) {
      // Not clean :|
      if (state.currentCutscene === "ms_pepper_pantry") {
        state.runCutsceneAfterNotificationAcknowledgement = false
        setTimeout(store.commit, 800, 'setDocumentationVisibility', true)
      }

      state.currentCutscene = undefined
    },
  }
})

export default store
