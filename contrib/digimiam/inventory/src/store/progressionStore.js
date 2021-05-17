import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

let store = new Vuex.Store({
  state: {
    displayDangerWindow: false,
    displayBlackScreen: true,
    isStocksOk: false,
  },
  mutations: {
    displayDangerWindow(state) {
      state.displayDangerWindow = true
    },
    displayBlackScreen(state, value) {
      state.displayBlackScreen = value
    },
    setIsStocksOk(state, value) {
      state.isStocksOk = value
    },
  },
})

export default store
