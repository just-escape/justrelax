import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

var store = new Vuex.Store({
  state: {
    initialGrids: {},
    currentGrids: {
      left: [
        'WWWWWWW.',
        'W.......',
        'W...W...',
        'W.......',
        'W..W....',
        'W.......',
        'W.......',
        'WWWWWWW.',
      ],
      front: [
        'WWWWWWW.',
        'W.......',
        'W.......',
        'W.......',
        'W.......',
        'W..WW...',
        'W.......',
        'WWWWWWW.',
      ],
      top: [
        'WWWWWWWW',
        'W......W',
        'W......W',
        'W...W..W',
        'W......W',
        'W......W',
        'W......W',
        'WWWWWWWW',
      ],
    },
    currentFace: 'left',
    currentLevel: 0,
  },
  mutations: {
    setFace(state, face) {
      state.currentFace = face
    },
    setLevel(state, level) {
      state.currentLevel = level
    }
  },
})

export default store
