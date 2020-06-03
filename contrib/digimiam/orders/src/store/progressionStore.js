import Vue from 'vue'
import Vuex from 'vuex'

import orderStore from '@/store/orderStore.js'

Vue.use(Vuex)

let store = new Vuex.Store({
  state: {
    round: 0,
    showDocumentation: false,
    isRestaurantClosed: false,
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
  }
})

export default store
