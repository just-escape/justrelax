import Vue from 'vue'
import Vuex from 'vuex'

import publishSubscribeService from '@/store/publishSubscribeService.js'

Vue.use(Vuex)

var store = new Vuex.Store({
  state: {
    dots: [
      {
        x: 550 / 2 + 230 * Math.cos(Math.PI / 180 * (60 * 1 - 30)),
        y: 550 / 2 + 230 * Math.sin(Math.PI / 180 * (60 * 1 - 30)),
        connected: false,
      },
      {
        x: 550 / 2 + 230 * Math.cos(Math.PI / 180 * (60 * 2 - 30)),
        y: 550 / 2 + 230 * Math.sin(Math.PI / 180 * (60 * 2 - 30)),
        connected: false,
      },
      {
        x: 550 / 2 + 230 * Math.cos(Math.PI / 180 * (60 * 3 - 30)),
        y: 550 / 2 + 230 * Math.sin(Math.PI / 180 * (60 * 3 - 30)),
        connected: false,
      },
      {
        x: 550 / 2 + 230 * Math.cos(Math.PI / 180 * (60 * 4 - 30)),
        y: 550 / 2 + 230 * Math.sin(Math.PI / 180 * (60 * 4 - 30)),
        connected: false,
      },
      {
        x: 550 / 2 + 230 * Math.cos(Math.PI / 180 * (60 * 5 - 30)),
        y: 550 / 2 + 230 * Math.sin(Math.PI / 180 * (60 * 5 - 30)),
        connected: false,
      },
      {
        x: 550 / 2 + 230 * Math.cos(Math.PI / 180 * (60 * 6 - 30)),
        y: 550 / 2 + 230 * Math.sin(Math.PI / 180 * (60 * 6 - 30)),
        connected: false,
      },
      {
        x: 550 / 2,
        y: 550 / 2,
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
    enableSuccess: false,
    boxOffsetTop: 0,
    boxOffsetLeft: 0,
  },
  mutations: {
    setBoxOffset(state, {top, left}) {
      state.boxOffsetTop = top
      state.boxOffsetLeft = left
    },
    enable(state) {
      state.enableSuccess = true
    },
    move(state, {x, y}) {
      state.cursorPosition.x = x - state.boxOffsetLeft
      state.cursorPosition.y = y - state.boxOffsetTop

      for (var i = 0 ; i < state.dots.length ; i++) {
        // 900 = 30^2
        if (Math.pow(state.dots[i].x - state.cursorPosition.x, 2) + Math.pow(state.dots[i].y - state.cursorPosition.y, 2) < 900) {
          store.commit('connect', i)

          if (state.enableSuccess) {
            store.commit('checkPattern')
            if (state.success) {
              store.commit('setConnectorsColorTransition', 0.8)
              store.commit('showSuccess')
              setTimeout(store.commit, 801, 'setConnectorsColorTransition', 0)
              setTimeout(store.commit, 1200, 'resetPattern')
              setTimeout(store.commit, 1200, 'notifySuccess')
            }
          }
        }
      }
    },
    startPattern(state, dotIndex) {
      if (state.lockActions) {
        return
      }

      if (state.lastConnectedDotIndex === null) {
        state.dots[dotIndex].connected = true
        state.lastConnectedDotIndex = dotIndex
        state.drawing = true
        state.cursorPosition.x = state.dots[dotIndex].x
        state.cursorPosition.y = state.dots[dotIndex].y
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
        publishSubscribeService.commit('publish', {category: 'success'})
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
