import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex);

export default new Vuex.Store({
  state: {
    displayNotificationPanel: false
  },
  mutations: {
    toggleDisplayNotificationPanel (state) {
      state.displayNotificationPanel = !state.displayNotificationPanel
    }
  },
  actions: {
    toggleDisplayNotificationPanel (context) {
      context.commit('toggleDisplayNotificationPanel')
    }
  }
})
