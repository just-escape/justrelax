import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

const INITIAL_GRID_EASY_LEFT = [
  'WWWWWWW.',
  'W.......',
  'W...W...',
  'W.......',
  'W..W....',
  'W.......',
  'W.......',
  'WWWWWWW.',
]

const INITIAL_BLOCKS_EASY_LEFT = [
  {
    x: 3,
    y: 4,
  },
]

const INITIAL_GRID_EASY_FRONT = [
  'WWWWWWW.',
  'W.......',
  'W.......',
  'W.......',
  'W.......',
  'W..WW...',
  'W.......',
  'WWWWWWW.',
]

const INITIAL_BLOCKS_EASY_FRONT = [
  {
    x: 3,
    y: 4,
  },
]

const INITIAL_GRID_EASY_TOP = [
  'WWWWWWWW',
  'W......W',
  'W......W',
  'W...W..W',
  'W......W',
  'W......W',
  'W......W',
  'WWWWWWWW',
]

const INITIAL_BLOCKS_EASY_TOP = [
  {
    x: 3,
    y: 4,
  },
]

const INITIAL_GRID_NORMAL_LEFT = [
  '........',
  'W.......',
  'W...W...',
  'W.......',
  'W..W....',
  'W.......',
  'W.......',
  '........',
]

const INITIAL_BLOCKS_NORMAL_LEFT = [
  {
    x: 3,
    y: 5,
  },
  {
    x: 4,
    y: 4,
  },
]

const INITIAL_GRID_NORMAL_FRONT = [
  '........',
  'W.......',
  'W.......',
  'W.......',
  'W.......',
  'W..WW...',
  'W.......',
  '........',
]

const INITIAL_BLOCKS_NORMAL_FRONT = [
  {
    x: 3,
    y: 4,
  },
  {
    x: 4,
    y: 4,
  },
]

const INITIAL_GRID_NORMAL_TOP = [
  '........',
  'W......W',
  'W......W',
  'W...W..W',
  'W......W',
  'W......W',
  'W......W',
  '........',
]

const INITIAL_BLOCKS_NORMAL_TOP = [
  {
    x: 3,
    y: 4,
  },
  {
    x: 4,
    y: 4,
  },
]

const INITIAL_GRID_HARD_LEFT = [
  '........',
  '.W...W..',
  '..W.W...',
  '...W....',
  '..W.W...',
  '.W...W..',
  '........',
  '........',
]

const INITIAL_BLOCKS_HARD_LEFT = [
  {
    x: 3,
    y: 4,
  },
]

const INITIAL_GRID_HARD_FRONT = [
  '........',
  '........',
  '........',
  '........',
  '........',
  '....W...',
  '........',
  '........',
]

const INITIAL_BLOCKS_HARD_FRONT = [
  {
    x: 3,
    y: 4,
  },
]

const INITIAL_GRID_HARD_TOP = [
  '........',
  '........',
  '...W.W..',
  '....W...',
  '...W.W..',
  '........',
  '........',
  '........',
]

const INITIAL_BLOCKS_HARD_TOP = [
  {
    x: 3,
    y: 4,
  },
]

var store = new Vuex.Store({
  state: {
    lockDifficulty: false,
    difficulty: 'normal',
    initialGrids: {
      easy: {
        left: INITIAL_GRID_EASY_LEFT,
        front: INITIAL_GRID_EASY_FRONT,
        top: INITIAL_GRID_EASY_TOP,
      },
      normal: {
        left: INITIAL_GRID_NORMAL_LEFT,
        front: INITIAL_GRID_NORMAL_FRONT,
        top: INITIAL_GRID_NORMAL_TOP,
      },
      hard: {
        left: INITIAL_GRID_HARD_LEFT,
        front: INITIAL_GRID_HARD_FRONT,
        top: INITIAL_GRID_HARD_TOP,
      },
    },
    initialBlocks: {
      easy: {
        left: INITIAL_BLOCKS_EASY_LEFT,
        front: INITIAL_BLOCKS_EASY_FRONT,
        top: INITIAL_BLOCKS_EASY_TOP,
      },
      normal: {
        left: INITIAL_BLOCKS_NORMAL_LEFT,
        front: INITIAL_BLOCKS_NORMAL_FRONT,
        top: INITIAL_BLOCKS_NORMAL_TOP,
      },
      hard: {
        left: INITIAL_BLOCKS_HARD_LEFT,
        front: INITIAL_BLOCKS_HARD_FRONT,
        top: INITIAL_BLOCKS_HARD_TOP,
      },
    },
    currentGrids: {
      left: INITIAL_GRID_NORMAL_LEFT,
      front: INITIAL_GRID_NORMAL_FRONT,
      top: INITIAL_GRID_NORMAL_TOP,
    },
    currentBlocks: {
      left: INITIAL_BLOCKS_NORMAL_LEFT,
      front: INITIAL_BLOCKS_NORMAL_FRONT,
      top: INITIAL_BLOCKS_NORMAL_TOP,
    },
    currentFace: 'left',
    currentLevel: 0,
    marmitronPosition: {
      x: 1,
      y: 1,
    },
    rows: 8,
    cols: 8,
  },
  mutations: {
    setFace(state, face) {
      state.currentFace = face
    },
    setLevel(state, level) {
      state.currentLevel = level
    },
    setDifficulty(state, difficulty) {
      if (["easy", "normal", "hard"].includes(difficulty)) {
        if (!state.lockDifficulty) {
          state.difficulty = difficulty
          state.currentGrids.left = state.initialGrids[difficulty].left
          state.currentGrids.front = state.initialGrids[difficulty].front
          state.currentGrids.top = state.initialGrids[difficulty].top
        }
      }
    },
    lockDifficulty(state) {
      state.lockDifficulty = true
    },
    move(state, direction) {
      if (["left", "right", "up", "down"].includes(direction)) {
        // The first move locks difficulty to ensure the map will not be changed during a game
        state.lockDifficulty = true
      }

      if (direction === "left") {
        let xAfterLeft = state.marmitronPosition.x - 1
        if (!isWalkableAt(xAfterLeft, state.marmitronPosition.y, "left")) {
          return
        } else {
          state.marmitronPosition.x = xAfterLeft
          moveBlockIfExist(
            state.marmitronPosition.x, state.marmitronPosition.y,
            state.marmitronPosition.x - 1, state.marmitronPosition.y,
          )
        }
      } else if (direction === "right") {
        let xAfterRight = state.marmitronPosition.x + 1
        if (!isWalkableAt(xAfterRight, state.marmitronPosition.y, "right")) {
          return
        } else {
          state.marmitronPosition.x = xAfterRight
          moveBlockIfExist(
            state.marmitronPosition.x, state.marmitronPosition.y,
            state.marmitronPosition.x + 1, state.marmitronPosition.y,
          )
        }
      } else if (direction === "up") {
        let yAfterUp = state.marmitronPosition.y - 1
        if (!isWalkableAt(state.marmitronPosition.x, yAfterUp, "up")) {
          return
        } else {
          state.marmitronPosition.y = yAfterUp
          moveBlockIfExist(
            state.marmitronPosition.x, state.marmitronPosition.y,
            state.marmitronPosition.x, state.marmitronPosition.y - 1,
          )
        }
      } else if (direction === "down") {
        let yAfterDown = state.marmitronPosition.y + 1
        if (!isWalkableAt(state.marmitronPosition.x, yAfterDown, "down")) {
          return
        } else {
          state.marmitronPosition.y = yAfterDown
          moveBlockIfExist(
            state.marmitronPosition.x, state.marmitronPosition.y,
            state.marmitronPosition.x, state.marmitronPosition.y + 1,
          )
        }
      }
    },
  },
})

function isWalkableAt(x, y, direction) {
  if (!(0 <= x && x < store.state.rows)) {
    return false
  }

  if (!(0 <= y && y < store.state.cols)) {
    return false
  }

  if (store.state.currentGrids[store.state.currentFace][y][x] === 'W') {
    return false
  }

  for (var block of store.state.currentBlocks[store.state.currentFace]) {
    if (block.x === x && block.y === y) {
      if (direction === 'left') {
        return isWalkableAt(x - 1, y, null)
      } else if (direction === 'right') {
        return isWalkableAt(x + 1, y, null)
      } else if (direction === 'up') {
        return isWalkableAt(x, y - 1, null)
      } else if (direction === 'down') {
        return isWalkableAt(x, y + 1, null)
      } else {
        return false
      }
    }
  }

  return true
}

function moveBlockIfExist(xOrig, yOrig, xDestination, yDestination) {
  for (var block of store.state.currentBlocks[store.state.currentFace]) {
    if (block.x === xOrig && block.y === yOrig) {
      block.x = xDestination
      block.y = yDestination
      return
    }
  }
}

export default store
