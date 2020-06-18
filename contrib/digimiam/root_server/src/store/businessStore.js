import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

let store = new Vuex.Store({
  state: {
    secretAnswers: [
      'biere'
    ],
    lastPressedCharacter: '',
    pressSignal: false,
    backspaceSignal: false,
    crSignal: false,
    displayPasswordWindow: false,
    displayPasswordRecoveryWindow: false,
    displayDangerWindow: false,
    success: false,
  },
  mutations: {
    press (state, character) {
      state.lastPressedCharacter = character
      state.pressSignal = !state.pressSignal
    },
    backspace (state) {
      state.backspaceSignal = !state.backspaceSignal
    },
    cr (state) {
      state.crSignal = !state.crSignal
    },
    displayPasswordWindow (state) {
      state.displayPasswordWindow = true
      // eslint-disable-next-line
      console.log('display', state.displayPasswordWindow)
    },
    hidePasswordWindow (state) {
      state.displayPasswordWindow = false
      // eslint-disable-next-line
      console.log('hide', state.displayPasswordWindow)
    },
    displayPasswordRecoveryWindow (state) {
      state.displayPasswordRecoveryWindow = true
    },
    hidePasswordRecoveryWindow (state) {
      state.displayPasswordRecoveryWindow = false
    },
    displayDangerWindow (state) {
      state.displayDangerWindow = true
    },
    hideDangerWindow (state) {
      state.displayDangerWindow = false
    },
    success (state) {
      state.success = true
    },
  }
})

export default store
