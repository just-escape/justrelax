import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex);

export default new Vuex.Store({
  state: {
    glitches: {},
    selectableAreas: [
      // units in percent
      {top: 8, left: 8, dish: "Steakfie", price: "1"},
      {top: 8, left: 31, dish: "Pizzage", price: "2"},
      {top: 8, left: 54, dish: "Gaufresque", price: "3"},
      {top: 8, left: 77, dish: "Puddy puddy", price: "4"},
      {top: 31, left: 8, dish: "Insectosteak", price: "5"},
      {top: 31, left: 31, dish: "Pizzalière", price: "6"},
      {top: 31, left: 54, dish: "Spider-gaufre", price: "7"},
      {top: 31, left: 77, dish: "PotjeVleesch", price: "8"},
      {top: 54, left: 8, dish: "Protobulle", price: "9"},
      {top: 54, left: 31, dish: "Cambraisienne", price: "10"},
      {top: 54, left: 54, dish: "Nano-gaufre", price: "11"},
      {top: 54, left: 77, dish: "Ch'tite gelée", price: "12"},
      {top: 77, left: 8, dish: "Salade Flamande", price: "13"},
      {top: 77, left: 31, dish: "Pizzalgue", price: "14"},
      {top: 77, left: 54, dish: "Gaufre fourêt", price: "15"},
      {top: 77, left: 77, dish: "Flubber", price: "16"},
    ],
    selectableAreaHeight: 15, // percentage
    selectableAreaWidth: 15, // percentage
    menuItems: [
      {
        cursorLeft: 0,
        cursorTop: 0,
        cursorWidth: 41,
        cursorHeight: 41,
        selectorZIndex: 10,
        /* Relative to the .selector-frame
           .selector-frame width + bootstrap col-8 width + margin-right + col margin + col margin
         */
        wireX2: 537 + 16 + 15 + 15,
        /* Tmp value */
        wireY2: 150,
        dish: null,
        price: null,
      },
      {
        cursorLeft: 200,
        cursorTop: 200,
        cursorWidth: 41,
        cursorHeight: 41,
        selectorZIndex: 10,
        /* Relative to the .selector-frame
           .selector-frame width + bootstrap col-8 width + margin-right + col margin + col margin
         */
        wireX2: 537 + 16 + 15 + 15,
        /* Tmp value */
        wireY2: 200,
        dish: null,
        price: null,
      },
      {
        cursorLeft: 100,
        cursorTop: 100,
        cursorWidth: 41,
        cursorHeight: 41,
        selectorZIndex: 10,
        /* Relative to the .selector-frame
           .selector-frame width + bootstrap col-8 width + margin-right + col margin + col margin
         */
        wireX2: 537 + 16 + 15 + 15,
        /* Tmp value */
        wireY2: 250,
        dish: null,
        price: null,
      },
      {
        cursorLeft: 50,
        cursorTop: 50,
        cursorWidth: 41,
        cursorHeight: 41,
        selectorZIndex: 10,
        /* Relative to the .selector-frame
           .selector-frame width + bootstrap col-8 width + margin-right + col margin + col margin
         */
        wireX2: 537 + 16 + 15 + 15,
        /* Tmp value */
        wireY2: 300,
        dish: null,
        price: null,
      },
    ],
    selectorHeight: 438,
    selectorWidth: 535.98,
    mouseX: 0,
    lastMouseX: null,
    mouseY: 0,
    lastMouseY: null,
    dragging: null,
    zIndexCounter: 10,
  },
  mutations: {
    // eslint-disable-next-line
    appMoving (state, event) {
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
            state.menuItems[state.dragging].price = state.selectableAreas[i].price
            return
          }
        }
        state.menuItems[state.dragging].dish = null
        state.menuItems[state.dragging].price = null
      }
    },
    appTapStart (state, id) {
      state.dragging = id
      state.zIndexCounter += 1
      state.menuItems[id].zIndex = state.zIndexCounter
    },
    appTapEnd (state) {
      state.dragging = null
    },
    appMouseleave (state) {
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
