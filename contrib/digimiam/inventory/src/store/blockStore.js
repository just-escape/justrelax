import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

var store = new Vuex.Store({
  state: {
    tableHeight: 900,
    tableWidth: 900,
    mouseX: 0,
    lastMouseX: null,
    mouseY: 0,
    lastMouseY: null,
    blocks: [
      {
        color: "#a02b00",
        backgroundPosition: "25% 75%",
        left: 0,
        top: 0,
        width: 150,
        height: 300,
        verticalDrag: true,
        horizontalDrag: false,
        zIndex: 10,
      },
      {
        color: "#a02b00",
        backgroundPosition: "75% 25%",
        left: 300,
        top: 0,
        width: 300,
        height: 150,
        verticalDrag: false,
        horizontalDrag: true,
        zIndex: 10,
      },
      {
        color: "#a02b00",
        backgroundPosition: "50% 75%",
        left: 0,
        top: 300,
        width: 300,
        height: 150,
        verticalDrag: false,
        horizontalDrag: true,
        zIndex: 10,
      },
      {
        color: "#a02b00",
        backgroundPosition: "32% 0%",
        left: 450,
        top: 450,
        width: 150,
        height: 150,
        verticalDrag: true,
        horizontalDrag: true,
        zIndex: 10,
      },
    ],
    dragging: null,
    zIndexCounter: 10,
  },
  mutations: {
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

        var i = 0
        if (state.blocks[state.dragging].horizontalDrag === true) {
          if (deltaX > 0) {
            // going right
            var firstObstacleLeft = state.tableWidth
            var draggedBlockRight = state.blocks[state.dragging].left + state.blocks[state.dragging].width

            for (i = 0 ; i < state.blocks.length ; i++) {
              if (state.dragging == i) {
                continue
              }

              if ((state.blocks[state.dragging].top >= state.blocks[i].top + state.blocks[i].height) ||
                  (state.blocks[state.dragging].top + state.blocks[state.dragging].height <= state.blocks[i].top)) {
                continue
              }

              if (draggedBlockRight > state.blocks[i].left) {
                continue
              }

              firstObstacleLeft = Math.min(firstObstacleLeft, state.blocks[i].left)
            }

            state.blocks[state.dragging].left = Math.min(state.blocks[state.dragging].left + deltaX, firstObstacleLeft - state.blocks[state.dragging].width)
          } else if (deltaX < 0) {
            // going left
            var firstObstacleRight = 0 // 0 is the left border
            var futureDraggedBlockLeft = state.blocks[state.dragging].left + deltaX

            for (i = 0 ; i < state.blocks.length ; i++) {
              if (state.dragging == i) {
                continue
              }

              var iBlockRight = state.blocks[i].left + state.blocks[i].width

              if ((state.blocks[state.dragging].top >= state.blocks[i].top + state.blocks[i].height) ||
                  (state.blocks[state.dragging].top + state.blocks[state.dragging].height <= state.blocks[i].top)) {
                continue
              }

              if (state.blocks[state.dragging].left < iBlockRight) {
                continue
              }

              firstObstacleRight = Math.max(firstObstacleRight, iBlockRight)
            }

            state.blocks[state.dragging].left = Math.max(futureDraggedBlockLeft, firstObstacleRight)
          }
        }

        if (state.blocks[state.dragging].verticalDrag === true) {
          if (deltaY > 0) {
            // going down
            var firstObstacleTop = state.tableHeight
            var draggedBlockBottom = state.blocks[state.dragging].top + state.blocks[state.dragging].height

            for (i = 0 ; i < state.blocks.length ; i++) {
              if (state.dragging == i) {
                continue
              }

              if ((state.blocks[state.dragging].left >= state.blocks[i].left + state.blocks[i].width) ||
                  (state.blocks[state.dragging].left + state.blocks[state.dragging].width <= state.blocks[i].left)) {
                continue
              }

              if (draggedBlockBottom > state.blocks[i].top) {
                continue
              }

              firstObstacleTop = Math.min(firstObstacleTop, state.blocks[i].top)
            }

            state.blocks[state.dragging].top = Math.min(state.blocks[state.dragging].top + deltaY, firstObstacleTop - state.blocks[state.dragging].height)
          } else if (deltaY < 0) {
            // going up
            var firstObstacleBottom = 0 // 0 is the top border
            var futureDraggedBlockTop = state.blocks[state.dragging].top + deltaY

            for (i = 0 ; i < state.blocks.length ; i++) {
              if (state.dragging == i) {
                continue
              }

              var iBlockBottom = state.blocks[i].top + state.blocks[i].height

              if ((state.blocks[state.dragging].left >= state.blocks[i].left + state.blocks[i].width) ||
                  (state.blocks[state.dragging].left + state.blocks[state.dragging].width <= state.blocks[i].left)) {
                continue
              }

              if (state.blocks[state.dragging].top < iBlockBottom) {
                continue
              }

              firstObstacleBottom = Math.max(firstObstacleBottom, iBlockBottom)
            }

            state.blocks[state.dragging].top = Math.max(futureDraggedBlockTop, firstObstacleBottom)
          }
        }
      }
    },
    blockMousedown (state, id) {
      state.dragging = id
      state.zIndexCounter += 1
      state.blocks[id].zIndex = state.zIndexCounter
    },
    appMouseup (state) {
      state.dragging = null
    },
    appMouseleave (state) {
      state.dragging = null
    },
  }
})

export default store
