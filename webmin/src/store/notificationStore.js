import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex);

export default new Vuex.Store({
  state: {
    notifications: [],
    notificationIndexer: 0
  },
  mutations: {
    pushNotification (state, {type, message}) {
      state.notifications.push(
        {
          "id": state.notificationIndexer,
          "message": message,
          "type": type,
        }
      )
      state.notificationIndexer = state.notificationIndexer + 1
    },
    clearNotification (state, id) {
      state.notifications = state.notifications.filter(
        function(n) {
          return n.id != id;
        }
      );
    }
  },
  actions: {
    pushNotification (context, message) {
      let type = 'info'
      context.commit('pushNotification', {type, message})
    },
    pushError (context, message) {
      let type = 'error'
      context.commit('pushNotification', {type, message})
    },
    clearNotification (context, id) {
      context.commit('clearNotification', id)
    }
  }
})
