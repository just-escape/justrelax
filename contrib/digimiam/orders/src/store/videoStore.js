import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

let store = new Vuex.Store({
  state: {
    overlayVideoId: undefined,
  },
  mutations: {
    setOverlayVideoId(state, videoId) {
      state.overlayVideoId = videoId
    },
  },
})

export default store
