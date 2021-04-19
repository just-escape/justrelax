import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

let store = new Vuex.Store({
  state: {
    displayDangerWindow: false,
    displayBlackScreen: true,
  },
  mutations: {
    displayDangerWindow(state) {
      state.displayDangerWindow = true
    },
    displayBlackScreen(state, value) {
      state.displayBlackScreen = value
    },
  }
})

export default store
