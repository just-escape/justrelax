import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

var store = new Vuex.Store({
  state: {
    difficulty: 'normal',
    EASY: 'easy',
    NORMAL: 'normal',
    HARD: 'hard',
  },
  mutations: {
    setDifficulty (state, difficulty) {
      if ([state.EASY, state.NORMAL, state.HARD].includes(difficulty)) {
        state.difficulty = difficulty
      }
    },
  },
})

export default store
