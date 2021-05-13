import Vue from 'vue'
import Vuex from 'vuex'

import publishSubscribeService from '@/store/publishSubscribeService.js'
import progressionStore from '@/store/progressionStore.js'
import menuLogStore from '@/store/menuLogStore.js'

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
    menuItems: [
      {
        cursorLeft: 190,
        cursorTop: 190,
        cursorWidth: 30,
        cursorHeight: 30,
        selectorZIndex: 10,
        wireX2: 803,
        wireY2: 135,
        dish: null,
        isDishValidated: false,
        price: 10,
      },
      {
        cursorLeft: 535,
        cursorTop: 300,
        cursorWidth: 30,
        cursorHeight: 30,
        selectorZIndex: 10,
        wireX2: 803,
        wireY2: 186,
        dish: null,
        isDishValidated: false,
        price: 11,
      },
      {
        cursorLeft: 362,
        cursorTop: 40,
        cursorWidth: 30,
        cursorHeight: 30,
        selectorZIndex: 10,
        wireX2: 803,
        wireY2: 237,
        dish: null,
        isDishValidated: false,
        price: 12,
      },
      {
        cursorLeft: 545,
        cursorTop: 210,
        cursorWidth: 30,
        cursorHeight: 30,
        selectorZIndex: 10,
        wireX2: 803,
        wireY2: 288,
        dish: null,
        isDishValidated: false,
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
    autoValidateDishes: false,
    displaySelectableAreas: true,
    displayGraduations: true,
    displayGraduationTexts: true,
    allDishesAreGoodButWrongPriceCounter: -1,
    wrongDishesCounter: -3,
  },
  getters: {
    isSuccess (state) {
      for (var menuItemIndex in state.menuItems) {
        if (state.menuItems[menuItemIndex].dish !== state.expectedMenu[menuItemIndex]) {
          return false
        }
      }
      return true
    },
    hintLog (state) {
      let goodDishesWrongPriceCounter = 0
      for (var menuItemIndex in state.menuItems) {
        if (state.expectedMenu.includes(state.menuItems[menuItemIndex].dish)) {
          goodDishesWrongPriceCounter++
        }
      }

      // eslint-disable-next-line
      console.log(goodDishesWrongPriceCounter, state.wrongDishesCounter, state.allDishesAreGoodButWrongPriceCounter)
      if (goodDishesWrongPriceCounter < 4) {
        state.wrongDishesCounter++

        var modulus = state.autoValidateDishes ? 8 : 3
        var counterThreshold = state.autoValidateDishes ? 1 : 0

        if (state.wrongDishesCounter % modulus === 0 && state.wrongDishesCounter >= counterThreshold) {
          if (goodDishesWrongPriceCounter === 0) {
            return 'no_dishes_can_be_produced'
          } else {
            return 'some_dishes_cannot_be_produced'
          }
        }
      } else {
        state.allDishesAreGoodButWrongPriceCounter++
        if (state.allDishesAreGoodButWrongPriceCounter % 3 === 0) {
          return 'dishes_need_to_have_good_prices'
        }
      }

      return null
    },
  },
  mutations: {
    setAutoValidateDishes (state, value) {
      state.autoValidateDishes = value

      if (!state.success) {
        // Update isDishValidated properties to remain consistant with the autoValidateDishes value
        var menuItemIndex
        if (value) {
          for (menuItemIndex in state.menuItems) {
            if (state.menuItems[menuItemIndex].dish === state.expectedMenu[menuItemIndex]) {
              state.menuItems[menuItemIndex].isDishValidated = true
            }
          }

          for (menuItemIndex in state.menuItems) {
            if (!state.menuItems[menuItemIndex].isDishValidated) {
              return
            }
          }
          // We reach those lines only if all dishes are validated
          state.success = true
          progressionStore.commit("setMenuServiceSuccess")
        } else {
          for (menuItemIndex in state.menuItems) {
            state.menuItems[menuItemIndex].isDishValidated = false
          }
        }
      }
    },
    setDisplaySelectableAreas (state, value) {
      state.displaySelectableAreas = value
    },
    setDisplayGraduations (state, value) {
      state.displayGraduations = value
    },
    setDisplayGraduationTexts (state, value) {
      state.displayGraduationTexts = value
    },
    // eslint-disable-next-line
    appCursorMove (state, event) {
      if (state.validating) {
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
        if (state.menuItems[state.dragging].isDishValidated) {
          return
        }

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
    pushMenuEntry (state, {itemIndex, getters}) {
      var dish
      if (state.menuItems[itemIndex].dish) {
        dish = state.menuItems[itemIndex].dish
      } else {
        dish = "error"
      }

      publishSubscribeService.commit('publish', {
        category: "set_menu_entry",
        index: itemIndex,
        dish: dish,
      })

      if (state.autoValidateDishes) {
        if (state.menuItems[itemIndex].dish == state.expectedMenu[itemIndex]) {
          state.menuItems[itemIndex].isDishValidated = true
        }

        if (getters.isSuccess) {
          state.success = true
          progressionStore.commit("setMenuServiceSuccess")
        } else {
          // Only take in consideration dishes that are not errors. Otherwise it would spam all the time.
          if (dish != "error") {
            let hintLog = getters.hintLog
            if (hintLog) {
              menuLogStore.commit("processLog", {logMessage: hintLog, level: "warning", useLocale: true})
            }
          }
        }
      }
    },
    lockValidate (state) {
      state.validating = true
    },
    unlockValidate (state) {
      state.validating = false
    },
    validateMenu (state, getters) {
      if (state.success || state.validating) {
        return
      }

      if (getters.isSuccess) {
        state.success = true
        for (var menuItemIndex in state.menuItems) {
          state.menuItems[menuItemIndex].isDishValidated = true
        }
        progressionStore.commit("setMenuServiceSuccess")
      } else {
        let hintLog = getters.hintLog
        if (hintLog) {
          menuLogStore.commit("processLog", {logMessage: hintLog, level: "warning", useLocale: true})
        }
      }
    },
    forceSuccess (state) {
      if (state.success) {
        return
      }

      state.success = true

      state.menuItems[0].cursorTop = 140
      state.menuItems[0].cursorLeft = 629
      state.menuItems[1].cursorTop = 327
      state.menuItems[1].cursorLeft = 118
      state.menuItems[2].cursorTop = 235
      state.menuItems[2].cursorLeft = 282
      state.menuItems[3].cursorTop = 40
      state.menuItems[3].cursorLeft = 437

      for (var menuItemIndex in state.menuItems) {
        state.menuItems[menuItemIndex].dish = state.expectedMenu[menuItemIndex]
        state.menuItems[menuItemIndex].isDishValidated = true
        publishSubscribeService.commit('publish', {
          category: "set_menu_entry",
          index: menuItemIndex,
          dish: state.expectedMenu[menuItemIndex],
        })
      }
      progressionStore.commit("setMenuServiceSuccess")
    },
    setMenuCursorPosition (state, position) {
      state.cursorPosition = position
    },
  },
})
