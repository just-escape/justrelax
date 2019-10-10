import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex);

export default new Vuex.Store({
  state: {
    tokens: [
      {
        cursorLeft: 0,
        cursorTop: 0,
        cursorWidth: 40,
        cursorHeight: 40,
        zIndex: 10,
        /* Relative to the .selector-frame
           .selector-frame width + bootstrap col-8 width + margin-right + col margin + col margin
         */
        wireX2: 537 + 16 + 15 + 15,
        /* Relative to .menu-container
           border bottom + padding bottom + first label bottom margin + 3 * (label height + label bottom margin) + label height / 2 */ 
        wireY2: 150,
      },
      {
        cursorLeft: 200,
        cursorTop: 200,
        cursorWidth: 40,
        cursorHeight: 40,
        zIndex: 10,
        /* Relative to the .selector-frame
           .selector-frame width + bootstrap col-8 width + margin-right + col margin + col margin
         */
        wireX2: 537 + 16 + 15 + 15,
        /* Relative to .menu-container
           border bottom + padding bottom + first label bottom margin + 2 * (label height + label bottom margin) + label height / 2 */ 
        wireY2: 200,
      },
      {
        cursorLeft: 100,
        cursorTop: 100,
        cursorWidth: 40,
        cursorHeight: 40,
        zIndex: 10,
        /* Relative to the .selector-frame
           .selector-frame width + bootstrap col-8 width + margin-right + col margin + col margin
         */
        wireX2: 537 + 16 + 15 + 15,
        /* Relative to .menu-container
           border bottom + padding bottom + first label bottom margin + 1 * (label height + label bottom margin) + label height / 2 */ 
        wireY2: 250,
      },
      {
        cursorLeft: 50,
        cursorTop: 50,
        cursorWidth: 40,
        cursorHeight: 40,
        zIndex: 10,
        /* Relative to the .selector-frame
           .selector-frame width + bootstrap col-8 width + margin-right + col margin + col margin
         */
        wireX2: 537 + 16 + 15 + 15,
        /* Relative to .menu-container
           border bottom + padding bottom + label bottom margin + label height / 2 */ 
        wireY2: 300,
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
    selectedMeals: [
      {
        label: null,
      },
      {
        label: null,
      },
      {
        label: null,
      },
      {
        label: null,
      },
    ],
  },
  mutations: {
    // eslint-disable-next-line
    appMousemove (state, event) {
      if (state.lastMouseX === null) {
        state.lastMouseX = event.clientX
      } else {
        state.lastMouseX = state.mouseX
      }

      if (state.lastMouseY === null) {
        state.lastMouseY = event.clientY
      } else {
        state.lastMouseY = state.mouseY
      }

      state.mouseX = event.clientX
      state.mouseY = event.clientY

      var deltaX = state.mouseX - state.lastMouseX
      var deltaY = state.mouseY - state.lastMouseY

      if (state.dragging !== null) {
        if (deltaX > 0) {
          // going right
          state.tokens[state.dragging].cursorLeft = Math.min(
            state.tokens[state.dragging].cursorLeft + deltaX,
            state.selectorWidth - state.tokens[state.dragging].cursorWidth
          )
        } else if (deltaX < 0) {
          // going left
          state.tokens[state.dragging].cursorLeft = Math.max(
            state.tokens[state.dragging].cursorLeft + deltaX,
            0
          )
        }

        if (deltaY > 0) {
          // going down
          state.tokens[state.dragging].cursorTop = Math.min(
            state.tokens[state.dragging].cursorTop + deltaY,
            state.selectorHeight - state.tokens[state.dragging].cursorHeight
          )
        } else if (deltaY < 0) {
          // going up
          state.tokens[state.dragging].cursorTop = Math.max(
            state.tokens[state.dragging].cursorTop + deltaY,
            0
          )
        }
      }
    },
    tokenMousedown (state, id) {
      state.dragging = id
      state.zIndexCounter += 1
      state.tokens[id].zIndex = state.zIndexCounter
    },
    appMouseup (state) {
      state.dragging = null
    },
    appMouseleave (state) {
      state.dragging = null
    },
  },
})
