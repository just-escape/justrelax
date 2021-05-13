import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

const store = new Vuex.Store({
  state: {
    sessionTime: null,
  },
  mutations: {
    setSessionTime (state, seconds) {
      state.sessionTime = seconds
    }
  },
})

export default store
