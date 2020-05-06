import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    glitches: {},
    selectableAreas: [
      // units in percent
      {top: 8, left: 8, dish: "steakfie"},
      {top: 8, left: 31, dish: "pizzage"},
      {top: 8, left: 54, dish: "gaufresque"},
      {top: 8, left: 77, dish: "puddy_puddy"},
      {top: 31, left: 8, dish: "insectosteak"},
      {top: 31, left: 31, dish: "pizzaliere"},
      {top: 31, left: 54, dish: "spider_gaufre"},
      {top: 31, left: 77, dish: "potjevleesch"},
      {top: 54, left: 8, dish: "protobulle"},
      {top: 54, left: 31, dish: "cambraisienne"},
      {top: 54, left: 54, dish: "nano_gaufre"},
      {top: 54, left: 77, dish: "chtite_gelee"},
      {top: 77, left: 8, dish: "salade_flamande"},
      {top: 77, left: 31, dish: "pizzalgue"},
      {top: 77, left: 54, dish: "gaufre_fouret"},
      {top: 77, left: 77, dish: "flubber"},
    ],
    selectableAreaHeight: 15, // percentage
    selectableAreaWidth: 15, // percentage
    menuItems: [
      {
        cursorLeft: 0,
        cursorTop: 0,
        cursorWidth: 30,
        cursorHeight: 30,
        selectorZIndex: 10,
        wireX2: 899,
        wireY2: 135,
        dish: null,
        price: 8,
      },
      {
        cursorLeft: 200,
        cursorTop: 200,
        cursorWidth: 30,
        cursorHeight: 30,
        selectorZIndex: 10,
        wireX2: 899,
        wireY2: 186,
        dish: null,
        price: 12,
      },
      {
        cursorLeft: 100,
        cursorTop: 100,
        cursorWidth: 30,
        cursorHeight: 30,
        selectorZIndex: 10,
        wireX2: 899,
        wireY2: 237,
        dish: null,
        price: 13,
      },
      {
        cursorLeft: 50,
        cursorTop: 50,
        cursorWidth: 30,
        cursorHeight: 30,
        selectorZIndex: 10,
        wireX2: 899,
        wireY2: 288,
        dish: null,
        price: 15,
      },
    ],
    selectorHeight: 410,
    selectorWidth: 852,
    mouseX: 0,
    lastMouseX: null,
    mouseY: 0,
    lastMouseY: null,
    dragging: null,
    zIndexCounter: 10,
  },
  mutations: {
    // eslint-disable-next-line
    appCursorMove (state, event) {
      var clientX
      var clientY
      if (event.targetTouches === undefined) {
        clientX = event.clientX
        clientY = event.clientY
      } else {
        clientX = event.targetTouches[0].clientX
        clientY = event.targetTouches[0].clientY
      }

      if (state.lastMouseX === null) {
        state.lastMouseX = clientX
      } else {
        state.lastMouseX = state.mouseX
      }

      if (state.lastMouseY === null) {
        state.lastMouseY = clientY
      } else {
        state.lastMouseY = state.mouseY
      }

      state.mouseX = clientX
      state.mouseY = clientY

      var deltaX = state.mouseX - state.lastMouseX
      var deltaY = state.mouseY - state.lastMouseY

      if (state.dragging !== null) {
        if (deltaX > 0) {
          // going right
          state.menuItems[state.dragging].cursorLeft = Math.min(
            state.menuItems[state.dragging].cursorLeft + deltaX,
            state.selectorWidth - state.menuItems[state.dragging].cursorWidth
          )
        } else if (deltaX < 0) {
          // going left
          state.menuItems[state.dragging].cursorLeft = Math.max(
            state.menuItems[state.dragging].cursorLeft + deltaX, 0)
        }

        if (deltaY > 0) {
          // going down
          state.menuItems[state.dragging].cursorTop = Math.min(
            state.menuItems[state.dragging].cursorTop + deltaY,
            state.selectorHeight - state.menuItems[state.dragging].cursorHeight
          )
        } else if (deltaY < 0) {
          // going up
          state.menuItems[state.dragging].cursorTop = Math.max(
            state.menuItems[state.dragging].cursorTop + deltaY, 0)
        }
      }

      if (state.dragging !== null) {
        var cursorCenterX = state.menuItems[state.dragging].cursorLeft + state.menuItems[state.dragging].cursorWidth / 2
        var cursorCenterY = state.menuItems[state.dragging].cursorTop + state.menuItems[state.dragging].cursorHeight / 2
        var cursorPercentX = cursorCenterX / state.selectorWidth * 100
        var cursorPercentY = cursorCenterY / state.selectorHeight * 100

        // Check for areas inclusion
        for (var i = 0 ; i < state.selectableAreas.length ; i++) {
          if (
            state.selectableAreas[i].left <= cursorPercentX &&
            cursorPercentX <= state.selectableAreas[i].left + state.selectableAreaWidth &&
            state.selectableAreas[i].top <= cursorPercentY &&
            cursorPercentY <= state.selectableAreas[i].top + state.selectableAreaHeight
          ) {
            state.menuItems[state.dragging].dish = state.selectableAreas[i].dish
            return
          }
        }
        state.menuItems[state.dragging].dish = null
      }
    },
    cursorPress (state, id) {
      state.dragging = id
      state.zIndexCounter += 1
      state.menuItems[id].zIndex = state.zIndexCounter
    },
    appCursorRelease (state) {
      state.lastMouseX = null
      state.lastMouseY = null
      state.dragging = null
    },
    appMouseleave (state) {
      state.lastMouseX = null
      state.lastMouseY = null
      state.dragging = null
    },
    initGlitchAnimation (state, animationId) {
      state.glitches[animationId] = {
        animation: 0,
        redShadow: false,
      }
    },
    setGlitchRedShadow (state, {animationId, value}) {
      state.glitches[animationId].redShadow = value
    },
    playGlitchAnimation (state, animationId) {
      state.glitches[animationId].animation.play()
    },
    interruptGlitchAnimation (state, animationId) {
      state.glitches[animationId].animation.pause()
      state.glitches[animationId].redShadow = false
      state.glitches[animationId].animation.seek(0)
    }
  },
})
