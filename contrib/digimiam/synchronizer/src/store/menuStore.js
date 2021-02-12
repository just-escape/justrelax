import Vue from 'vue'
import Vuex from 'vuex'

import publishSubscribeService from '@/store/publishSubscribeService.js'
import progressionStore from '@/store/progressionStore.js'

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
      {top: 77, left: 54, dish: "algaufre"},
      {top: 77, left: 77, dish: "flubber"},
    ],
    selectableAreaHeight: 15, // percentage
    selectableAreaWidth: 15, // percentage
    graduations: [
      {
        dashLeft: "-5px",
        dashBottom: "15.5%",
        dashHeight: "1px",
        dashWidth: "5px",
        iconFa: false,
        icon: require("@/assets/img/seaweed.png"),
        iconLeft: "calc(-20px - 5px)",
        iconBottom: "calc(-16px / 2 + 0.5px)",
      },
      {
        dashLeft: "-5px",
        dashBottom: "38.5%",
        dashHeight: "1px",
        dashWidth: "5px",
        iconFa: true,
        icon: "fas fa-search",
        iconLeft: "calc(-20px - 5px)",
        iconBottom: "calc(-16px / 2 + 0.5px)",
      },
      {
        dashLeft: "-5px",
        dashBottom: "61.5%",
        dashHeight: "1px",
        dashWidth: "5px",
        iconFa: true,
        icon: "fas fa-bug",
        iconLeft: "calc(-20px - 5px)",
        iconBottom: "calc(-16px / 2 + 0.5px)",
      },
      {
        dashLeft: "-5px",
        dashBottom: "84.5%",
        dashHeight: "1px",
        dashWidth: "5px",
        iconFa: true,
        icon: "fas fa-smile",
        iconLeft: "calc(-20px - 5px)",
        iconBottom: "calc(-16px / 2 + 0.5px)",
      },
      {
        dashLeft: "15.5%",
        dashBottom: "-5px",
        dashHeight: "5px",
        dashWidth: "1px",
        iconFa: true,
        icon: "fa fa-drumstick-bite",
        iconLeft: "calc(-20px / 2 + 0.5px)",
        iconBottom: "calc(-16px - 5px)",
      },
      {
        dashLeft: "38.5%",
        dashBottom: "-5px",
        dashHeight: "5px",
        dashWidth: "1px",
        iconFa: true,
        icon: "fas fa-pizza-slice",
        iconLeft: "calc(-20px / 2 + 0.5px)",
        iconBottom: "calc(-16px - 5px)",
      },
      {
        dashLeft: "61.5%",
        dashBottom: "-5px",
        dashHeight: "5px",
        dashWidth: "1px",
        iconFa: false,
        icon: require("@/assets/img/waffle.png"),
        iconLeft: "calc(-20px / 2 + 0.5px)",
        iconBottom: "calc(-16px - 5px)",
      },
      {
        dashLeft: "84.5%",
        dashBottom: "-5px",
        dashHeight: "5px",
        dashWidth: "1px",
        iconFa: false,
        icon: require("@/assets/img/jelly.svg"),
        iconLeft: "calc(-20px / 2 + 0.5px)",
        iconBottom: "calc(-16px - 5px)",
      },
    ],
    menuItems: [
      {
        cursorLeft: 200,
        cursorTop: 170,
        cursorWidth: 30,
        cursorHeight: 30,
        selectorZIndex: 10,
        wireX2: 803,
        wireY2: 135,
        dish: null,
        price: 10,
      },
      {
        cursorLeft: 520,
        cursorTop: 300,
        cursorWidth: 30,
        cursorHeight: 30,
        selectorZIndex: 10,
        wireX2: 803,
        wireY2: 186,
        dish: null,
        price: 11,
      },
      {
        cursorLeft: 350,
        cursorTop: 40,
        cursorWidth: 30,
        cursorHeight: 30,
        selectorZIndex: 10,
        wireX2: 803,
        wireY2: 237,
        dish: null,
        price: 12,
      },
      {
        cursorLeft: 511,
        cursorTop: 266,
        cursorWidth: 30,
        cursorHeight: 30,
        selectorZIndex: 10,
        wireX2: 803,
        wireY2: 288,
        dish: null,
        price: 4,
      },
    ],
    expectedMenu: [
      "potjevleesch",
      "salade_flamande",
      "cambraisienne",
      "gaufresque",
    ],
    cursorPosition: 0,
    selectorHeight: 410,
    selectorWidth: 756,
    mouseX: 0,
    lastMouseX: null,
    mouseY: 0,
    lastMouseY: null,
    dragging: null,
    zIndexCounter: 10,
    validating: false,
    success: false,
  },
  getters: {
    isSuccess (state) {
      for (var menuItemIndex in state.menuItems) {
        if (state.menuItems[menuItemIndex].dish !== state.expectedMenu[menuItemIndex]) {
          return false
        }
      }
      return true
    }
  },
  mutations: {
    // eslint-disable-next-line
    appCursorMove (state, event) {
      if (state.success || state.validating) {
        return
      }

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
    },
    pushMenuEntry (state, index) {
      var dish
      if (state.menuItems[index].dish) {
        dish = state.menuItems[index].dish
      } else {
        dish = "error"
      }

      publishSubscribeService.commit('sendEvent', {
        category: "set_menu_entry",
        index: index,
        dish: dish,
      })
    },
    lockValidate (state) {
      state.validating = true
    },
    unlockValidate (state) {
      state.validating = false
    },
    validateMenu (state) {
      if (state.success || state.validating) {
        return
      }

      state.success = true
      progressionStore.commit("setMenuServiceSuccess")
    },
    forceSuccess (state) {
      if (state.success) {
        return
      }

      // TODO: set cursor positions ?
      // TODO: set menu entries
      // TODO: notify hologram player

      state.success = true
      /*publishSubscribeService.commit('sendEvent', {
        category: "menu_success"
      })*/
    },
    setMenuCursorPosition (state, position) {
      state.cursorPosition = position
    },
  },
})
