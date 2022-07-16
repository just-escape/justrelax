import Vue from 'vue'
import Vuex from 'vuex'

import publishSubscribeService from '@/store/publishSubscribeService.js'
import progressionStore from '@/store/progressionStore.js'

Vue.use(Vuex)

let store = new Vuex.Store({
  state: {
    glitches: {},
    lastChangedItemIndex: 0,
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
    dishesComposition: {
      "steakfie": {rowIndex: 0, columnIndex: 0, rowLabel: 'Portrait', columnLabel: 'Viande', pronoun: 'un steakfie'},
      "pizzage": {rowIndex: 0, columnIndex: 1, rowLabel: 'Portrait', columnLabel: 'Pizza', pronoun: 'une pizzage'},
      "gaufresque": {rowIndex: 0, columnIndex: 2, rowLabel: 'Portrait', columnLabel: 'Gaufre', pronoun: 'une gaufresque'},
      "puddy_puddy": {rowIndex: 0, columnIndex: 3, rowLabel: 'Portrait', columnLabel: 'Gelée', pronoun: 'un puddy puddy'},
      "insectosteak": {rowIndex: 1, columnIndex: 0, rowLabel: 'Insecte', columnLabel: 'Viande', pronoun: 'un insectosteak'},
      "pizzaliere": {rowIndex: 1, columnIndex: 1, rowLabel: 'Insecte', columnLabel: 'Pizza', pronoun: 'une pizzalière'},
      "spider_gaufre": {rowIndex: 1, columnIndex: 2, rowLabel: 'Insecte', columnLabel: 'Gaufre', pronoun: 'une spidergaufre'},
      "potjevleesch": {rowIndex: 1, columnIndex: 3, rowLabel: 'Insecte', columnLabel: 'Gelée', pronoun: 'un potjevleesch'},
      "protobulle": {rowIndex: 2, columnIndex: 0, rowLabel: 'Micro', columnLabel: 'Viande', pronoun: 'une protobulle'},
      "cambraisienne": {rowIndex: 2, columnIndex: 1, rowLabel: 'Micro', columnLabel: 'Pizza', pronoun: 'une cambraisienne'},
      "nano_gaufre": {rowIndex: 2, columnIndex: 2, rowLabel: 'Micro', columnLabel: 'Gaufre', pronoun: 'une nano-gaufre'},
      "chtite_gelee": {rowIndex: 2, columnIndex: 3, rowLabel: 'Micro', columnLabel: 'Gelée', pronoun: 'une cht\'tite gelée'},
      "salade_flamande": {rowIndex: 3, columnIndex: 0, rowLabel: 'Algue', columnLabel: 'Viande', pronoun: 'une salade flamande'},
      "pizzalgue": {rowIndex: 3, columnIndex: 1, rowLabel: 'Algue', columnLabel: 'Pizza', pronoun: 'une pizzalgue'},
      "algaufre": {rowIndex: 3, columnIndex: 2, rowLabel: 'Algue', columnLabel: 'Gaufre', pronoun: 'une algaufre'},
      "flubber": {rowIndex: 3, columnIndex: 3, rowLabel: 'Algue', columnLabel: 'Gelée', pronoun: 'un flubber'},
    },
    menuItems: [
      {
        id: 1,
        cursorLeft: 260,
        cursorTop: 37,
        cursorWidth: 114,
        cursorHeight: 59,
        selectorZIndex: 10,
        dish: "pizzage",
        isDishValidated: false,
        price: 10,
      },
      {
        id: 2,
        cursorLeft: 640,
        cursorTop: 58,
        cursorWidth: 114,
        cursorHeight: 59,
        selectorZIndex: 10,
        dish: "puddy_puddy",
        isDishValidated: false,
        price: 11,
      },
      {
        id: 3,
        cursorLeft: 600,
        cursorTop: 330,
        cursorWidth: 114,
        cursorHeight: 59,
        selectorZIndex: 10,
        dish: "flubber",
        isDishValidated: false,
        price: 12,
      },
      {
        id: 4,
        cursorLeft: 100,
        cursorTop: 225,
        cursorWidth: 114,
        cursorHeight: 59,
        selectorZIndex: 10,
        dish: "protobulle",
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
    selectorHeight: 395,
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
    displayPrice: false,
    priceMatters: true,
    displayMenuExplicitInstruction: false,
    onMenuChangedSignal: false,
    explainOnDishChangedCounter: 1,
  },
  getters: {
    isSuccess (state) {
      if (state.priceMatters) {
        for (var menuItemIndex in state.menuItems) {
          if (state.menuItems[menuItemIndex].dish !== state.expectedMenu[menuItemIndex]) {
            return false
          }
        }
      } else {
        for (let expectedMenuItem of state.expectedMenu) {
          if (!state.menuItems.map(menuItem => menuItem.dish).includes(expectedMenuItem)) {
            return false
          }
        }
      }
      return true
    },
  },
  mutations: {
    setExplainOnDishChangedCounter(state, value) {
      state.explainOnDishChangedCounter = value
      publishSubscribeService.commit('publish', {category: 'set_session_data', key: 'synchronizer_explain_on_dish_changed_counter', data: state.explainOnDishChangedCounter})
    },
    publishSessionData(state) {
      publishSubscribeService.commit('publish', {category: 'set_session_data', key: 'synchronizer_auto_validate_dishes', data: state.autoValidateDishes})
      publishSubscribeService.commit('publish', {category: 'set_session_data', key: 'synchronizer_display_price', data: state.displayPrice})
      publishSubscribeService.commit('publish', {category: 'set_session_data', key: 'synchronizer_price_matters', data: state.priceMatters})
      publishSubscribeService.commit('publish', {category: 'set_session_data', key: 'synchronizer_display_menu_explicit_instruction', data: state.displayMenuExplicitInstruction})
      publishSubscribeService.commit('publish', {category: 'set_session_data', key: 'synchronizer_explain_on_dish_changed_counter', data: state.explainOnDishChangedCounter})
    },
    setDisplayMenuExplicitInstruction(state, value) {
      state.displayMenuExplicitInstruction = value
      publishSubscribeService.commit('publish', {category: 'set_session_data', key: 'synchronizer_display_menu_explicit_instruction', data: state.displayMenuExplicitInstruction})
    },
    setPriceMatters(state, value) {
      state.priceMatters = value
      publishSubscribeService.commit('publish', {category: 'set_session_data', key: 'synchronizer_price_matters', data: state.priceMatters})
    },
    setAutoValidateDishes (state, value) {
      state.autoValidateDishes = value
      publishSubscribeService.commit('publish', {category: 'set_session_data', key: 'synchronizer_auto_validate_dishes', data: state.autoValidateDishes})

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
    setDisplayPrice (state, value) {
      state.displayPrice = value
      publishSubscribeService.commit('publish', {category: 'set_session_data', key: 'synchronizer_display_price', data: state.displayPrice})
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
      if (state.dragging !== null) {
        store.commit("pushMenuEntry", {itemIndex: state.dragging, onManualMode: false, getters: store.getters})  // TODO: do it elsewhere
      }
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
    pushMenuEntry (state, {itemIndex, onManualMode, getters}) {
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
        on_manual_mode: onManualMode,
      })

      state.onMenuChangedSignal = !state.onMenuChangedSignal
      state.lastChangedItemIndex = itemIndex

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
            store.commit('checkForMenuHintLog')
          }
        }
      }
    },
    checkForMenuHintLog(state) {
      publishSubscribeService.commit('publish', {
        'category': 'check_for_menu_hint_log',
        'dishes': state.menuItems.map(menuItem => menuItem.dish),
        'auto_validate_dishes': state.autoValidateDishes,
      })
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
        store.commit('checkForMenuHintLog')
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

export default store
