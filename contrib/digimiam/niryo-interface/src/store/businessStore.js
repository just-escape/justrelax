import Vue from 'vue'
import Vuex from 'vuex'
import justSockService from '@/store/justSockService.js'

Vue.use(Vuex)

var store = new Vuex.Store({
  state: {
    rows: [
      {
        title: "Emplacement 1",
        tokens: ["a", "b", "c", "d", "e", "f", "g", "h"],
        goodToken: "a",
        selectedTokenIndex: -1,
        selectionError: false,
        timeUnits: [false, false, false, false, false],
      },
      {
        title: "Emplacement 2",
        tokens: ["a", "b", "c", "d", "e", "f", "g", "h"],
        goodToken: "a",
        selectedTokenIndex: -1,
        selectionError: false,
        timeUnits: [false, false, false, false, false],
      },
      {
        title: "Emplacement 3",
        tokens: ["a", "b", "c", "d", "e", "f", "g", "h"],
        goodToken: "a",
        selectedTokenIndex: -1,
        selectionError: false,
        timeUnits: [false, false, false, false, false],
      },
      {
        title: "Emplacement 4",
        tokens: ["a", "b", "c", "d", "e", "f", "g", "h"],
        goodToken: "a",
        selectedTokenIndex: -1,
        selectionError: false,
        timeUnits: [false, false, false, false, false],
      },
      {
        title: "Emplacement 5",
        tokens: ["a", "b", "c", "d", "e", "f", "g", "h"],
        goodToken: "a",
        selectedTokenIndex: -1,
        selectionError: false,
        timeUnits: [false, false, false, false, false],
      },
    ],
    currentRowIndex: 0,
    configurations: {
      a: [
        [true, false, false],
        [true, false, false],
        [true, false, false]
      ],
      b: [
        [true, false, false],
        [true, true, false],
        [true, false, false]
      ],
      c: [
        [false, false, false],
        [true, false, false],
        [true, true, false]
      ],
      d: [
        [false, false, false],
        [true, true, false],
        [false, true, false]
      ],
      e: [
        [false, true, false],
        [true, true, true],
        [false, true, false]
      ],
      f: [
        [false, false, false],
        [true, true, true],
        [false, true, false]
      ],
      g: [
        [false, true, false],
        [true, true, true],
        [false, false, false]
      ],
      h: [
        [false, true, true],
        [false, true, true],
        [false, false, false]
      ],
    },
    gameLost: false,
  },
  mutations: {
    setSelectedToken(state, {rowIndex, tokenIndex}) {
      if (state.gameLost) {
        return
      }

      state.rows[rowIndex].selectedTokenIndex = tokenIndex

      if (rowIndex > state.currentRowIndex) {
        state.rows[rowIndex].selectionError = true
        state.gameLost = true
      } else if (state.rows[rowIndex].tokens[state.rows[rowIndex].selectedTokenIndex] !== state.rows[rowIndex].goodToken) {
        state.rows[rowIndex].selectionError = true
        state.gameLost = true
      } else if (rowIndex === state.currentRowIndex) {
        for (var i = 0 ; i < state.rows[state.currentRowIndex].timeUnits.length ; i++) {
          Vue.set(state.rows[state.currentRowIndex].timeUnits, i, true)
        }
        state.currentRowIndex++
        if (state.currentRowIndex < state.rows.length) {
          justSockService.commit('sendEvent', state.rows[state.currentRowIndex].goodToken)
        } else {
          window.location.href = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
        }
      }
    },
    ticTac(state) {
      if (state.gameLost) {
        return
      }

      for (var i = 0 ; i < state.rows[state.currentRowIndex].timeUnits.length ; i++) {
        if (state.rows[state.currentRowIndex].timeUnits[i] === false) {
          Vue.set(state.rows[state.currentRowIndex].timeUnits, i, true)
          return
        }
      }
    },
    currentRowIndexPlusPlus(state) {
      state.currentRowIndex++
    },
    setGameLost(state) {
      state.gameLost = true
    },
    shuffle(state) {
      for (var row of state.rows) {
        row.tokens = row.tokens.sort(() => Math.random() - 0.5)
        row.goodToken = row.tokens[Math.floor(Math.random() * (row.tokens.length - 1))]
      }
    },
  },
  actions: {
    startGame(context) {
      context.commit('shuffle')
      justSockService.commit('sendEvent', context.state.rows[context.state.currentRowIndex].goodToken)
      setTimeout(context.dispatch, 2000, 'ticTac')
    },
    ticTac(context) {
      if (context.state.gameLost) {
        return
      }

      context.commit('ticTac')
      let currentRow = context.state.rows[context.state.currentRowIndex]
      var atLeastOneTULeft = false
      for (var tu of currentRow.timeUnits) {
        if (tu === false) {
          atLeastOneTULeft = true
          break
        }
      }

      if (!atLeastOneTULeft) {
        if (context.state.currentRowIndex >= context.state.rows.length) {
          context.commit('setGameLost')
        } else if (context.state.rows[context.state.currentRowIndex].tokens[context.state.rows[context.state.currentRowIndex].selectedTokenIndex] !== context.state.rows[context.state.currentRowIndex].goodToken) {
          context.commit('setGameLost')
        } else {
          context.commit('currentRowIndexPlusPlus')
        }
      }

      if (context.state.currentRowIndex === context.state.rows.length) {
        context.commit('setGameLost')
      } else {
        setTimeout(context.dispatch, 2000, 'ticTac')
      }
    },
  },
})

export default store
