import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex);

export default new Vuex.Store({
  state: {
    notifications: [],
    notificationIndexer: 0
  },
  mutations: {
    displayNotification (state, content) {
      state.notifications.push(
        {
          "id": state.notificationIndexer,
          "content": content
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
    displayNotification (context, content) {
      context.commit('displayNotification', content)
    },
    clearNotification (context, id) {
      context.commit('clearNotification', id)
    }
  }
})
