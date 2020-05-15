import Vue from 'vue'
import Vuex from 'vuex'

import justSockService from '@/store/justSockService.js'

Vue.use(Vuex)

var store = new Vuex.Store({
  state: {
    dots: [
      {
        x: 550 / 2,
        y: 69,
        connected: false,
      },
      {
        x: 430 + 60,
        y: 496 * 1 / 4 + 69,
        connected: false,
      },
      {
        x: 430 + 60,
        y: 496 * 3 / 4 + 69,
        connected: false,
      },
      {
        x: 550 / 2,
        y: 496 + 69,
        connected: false,
      },
      {
        x: 60,
        y: 496 * 3 / 4 + 69,
        connected: false,
      },
      {
        x: 60,
        y: 496 * 1 / 4 + 69,
        connected: false,
      },
      {
        x: 550 / 2,
        y: 635 / 2,
        connected: false,
      },
    ],
    connections: [],
    lastConnectedDotIndex: null,
    cursorPosition: {
      x: 0,
      y: 0,
    },
    connectorsColor: {
      r: 255,
      g: 255,
      b: 255,
    },
    connectorsColorTransition: 0.8,
    lockActions: false,
    showErrorOnRealse: false,
    drawing: false,
    successPattern: [
      [4, 5],
      [5, 6],
      [6, 1],
      [1, 2],
    ],
    success: false,
    successNotified: false,
  },
  mutations: {
    move(state, {x, y}) {
      state.cursorPosition.x = x
      state.cursorPosition.y = y
    },
    startPattern(state, dotIndex) {
      if (state.lockActions) {
        return
      }

      if (state.lastConnectedDotIndex === null) {
        state.dots[dotIndex].connected = true
        state.lastConnectedDotIndex = dotIndex
        state.drawing = true
      }
    },
    connect(state, dotIndex) {
      if (state.lockActions) {
        return
      }

      if (state.drawing) {
        if (state.lastConnectedDotIndex === dotIndex) {
          return
        }

        for (var connection of state.connections) {
          if (
            (connection[0] === dotIndex && connection[1] === state.lastConnectedDotIndex) ||
            (connection[1] === dotIndex && connection[0] === state.lastConnectedDotIndex)
          ) {
            // This connection has already been recorded. Connections cannot happen twice.
            return
          }
        }

        state.dots[dotIndex].connected = true
        state.connections.push([state.lastConnectedDotIndex, dotIndex])
        state.lastConnectedDotIndex = dotIndex
        state.showErrorOnRealse = true
      }
    },
    checkPattern(state) {
        console.log(state.connections, state.successPattern)
      if (state.successPattern.length !== state.connections.length) {
        return
      }

      for (var i = 0 ; i < state.successPattern.length ; i++) {
        if (state.successPattern[i][0] !== state.connections[i][0]) {
          return
        }

        if (state.successPattern[i][1] !== state.connections[i][1]) {
          return
        }
      }

      // Otherwise
      state.success = true
    },
    notifySuccess(state) {
      if (!state.successNotified) {
        state.successNotified = true
        justSockService.commit('sendEvent', {category: 'success'})
      }
    },
    setConnectorsColorTransition(state, value) {
      state.connectorsColorTransition = value
    },
    showSuccess(state) {
      state.drawing = false
      state.lockActions = true
      state.connectorsColor.r = 0
      state.connectorsColor.g = 170
      state.connectorsColor.b = 0
    },
    showError(state) {
      state.drawing = false
      state.lockActions = true
      state.connectorsColor.r = 255
      state.connectorsColor.g = 0
      state.connectorsColor.b = 0
    },
    resetPattern(state) {
      state.lockActions = false
      state.connectorsColor.r = 255
      state.connectorsColor.g = 255
      state.connectorsColor.b = 255

      for (var i = 0 ; i < state.dots.length ; i++) {
        state.dots[i].connected = false 
      }

      state.drawing = false
      state.lastConnectedDotIndex = null
      state.connections = []
      state.showErrorOnRealse = false
      state.success = false
    }
  },
})

export default store
