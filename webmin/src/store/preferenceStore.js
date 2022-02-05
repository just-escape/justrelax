import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    displayNotificationPanel: false,
    isInMaintenanceMode: false,
  },
  mutations: {
    toggleDisplayNotificationPanel (state) {
      state.displayNotificationPanel = !state.displayNotificationPanel
    },
    setMaintenanceMode (state, value) {
      state.isInMaintenanceMode = value
    },
  },
  actions: {
    toggleDisplayNotificationPanel (context) {
      context.commit('toggleDisplayNotificationPanel')
    }
  }
})
