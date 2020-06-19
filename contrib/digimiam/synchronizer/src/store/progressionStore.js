import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

let store = new Vuex.Store({
  state: {
    displayDangerWindow: false,
  },
  mutations: {
    displayDangerWindow(state) {
      state.displayDangerWindow = true
    },
  }
})

export default store
