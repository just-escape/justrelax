import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

const INITIAL_GRID_TUTORIAL_1 = [
  'WWWWW1W',
  'W.....R',
  'W.W.W.W',
  'W.....W',
  'W.W.W.W',
  'W.....0',
  'WWWWWWW',
]

const INITIAL_BLOCKS_TUTORIAL_1 = [
  {
    x: 5,
    y: 5,
  },
  {
    x: 5,
    y: 1,
  },
]

const INITIAL_GRID_TUTORIAL_1_LOWER_PASSAGE = [
  'WWWWW1W',
  'W.....W',
  'W.W.W.W',
  'W.....R',
  'W.W.W.W',
  'W.....0',
  'WWWWWWW',
]

const INITIAL_GRID_TUTORIAL_2 = [
  'WWWUWWW',
  'L.....W',
  'W..W4.W',
  'W..3..W',
  'W.2W..W',
  'W.....W',
  'WWWWWWW',
]

const INITIAL_BLOCKS_TUTORIAL_2 = [
  {
    x: 2,
    y: 2,
  },
  {
    x: 4,
    y: 3,
  },
  {
    x: 4,
    y: 4,
  },
]

const INITIAL_GRID_SOKOGEN_4_ROTATE_180 = [
  'WWWWWWW',
  'WW.4.WW',
  'W..3..W',
  'W..2..W',
  'W..W..W',
  'WW...WW',
  'WWWDWWW',
]

const INITIAL_BLOCKS_SOKOGEN_4_ROTATE_180 = [
  {
    x: 2,
    y: 3,
  },
  {
    x: 3,
    y: 3,
  },
  {
    x: 4,
    y: 3,
  },
]

const INITIAL_GRID_SOKOGEN_4_ROTATE_270 = [
  'WWWUWWW',
  'WW...WW',
  'W.....W',
  'L.W234W',
  'W.....W',
  'WW...WW',
  'WWWWWWW',
]

const INITIAL_BLOCKS_SOKOGEN_4_ROTATE_270 = [
  {
    x: 3,
    y: 2,
  },
  {
    x: 3,
    y: 3,
  },
  {
    x: 3,
    y: 4,
  },
]

const INITIAL_GRID_SOKOGEN_11 = [
  'WWWWWWW',
  'W...WWW',
  'W.W.WWW',
  'W56...W',
  'W..W..W',
  'W....7W',
  'WWWDWWW',
]

const INITIAL_BLOCKS_SOKOGEN_11 = [
  {
    x: 1,
    y: 3,
  },
  {
    x: 3,
    y: 3,
  },
  {
    x: 4,
    y: 4,
  },
]

const INITIAL_GRID_SOKOGEN_11_UPSIDE_DOWN = [
  'WWWWUWW',
  'L....4W',
  'W..W..W',
  'W23...W',
  'W.W.WWW',
  'W...WWW',
  'WWWWWWW',
]

const INITIAL_BLOCKS_SOKOGEN_11_UPSIDE_DOWN = [
  {
    x: 1,
    y: 3,
  },
  {
    x: 3,
    y: 3,
  },
  {
    x: 4,
    y: 2,
  },
]

const INITIAL_GRID_SOKOGEN_28 = [
  'WWWWWWW',
  'W...WWW',
  'W.W.WWW',
  'W7....W',
  'W6..W.W',
  'W..5..W',
  'WWWWDWW',
]

const INITIAL_BLOCKS_SOKOGEN_28 = [
  {
    x: 3,
    y: 3,
  },
  {
    x: 4,
    y: 3,
  },
  {
    x: 3,
    y: 5,
  },
]

var store = new Vuex.Store({
  state: {
    lockDifficulty: false,
    difficulty: 'normal',
    grids: {
      easy: {
        left: INITIAL_GRID_TUTORIAL_1,
        front: INITIAL_GRID_TUTORIAL_2,
        top: INITIAL_GRID_SOKOGEN_4_ROTATE_180,
      },
      normal: {
        left: INITIAL_GRID_TUTORIAL_1_LOWER_PASSAGE,
        front: INITIAL_GRID_SOKOGEN_4_ROTATE_270,
        top: INITIAL_GRID_SOKOGEN_11,
      },
      hard: {
        left: INITIAL_GRID_TUTORIAL_1,
        front: INITIAL_GRID_SOKOGEN_11_UPSIDE_DOWN,
        top: INITIAL_GRID_SOKOGEN_28,
      },
    },
    initialBlocks: {
      easy: {
        left: INITIAL_BLOCKS_TUTORIAL_1,
        front: INITIAL_BLOCKS_TUTORIAL_2,
        top: INITIAL_BLOCKS_SOKOGEN_4_ROTATE_180,
      },
      normal: {
        left: INITIAL_BLOCKS_TUTORIAL_1,
        front: INITIAL_BLOCKS_SOKOGEN_4_ROTATE_270,
        top: INITIAL_BLOCKS_SOKOGEN_11,
      },
      hard: {
        left: INITIAL_BLOCKS_TUTORIAL_1,
        front: INITIAL_BLOCKS_SOKOGEN_11_UPSIDE_DOWN,
        top: INITIAL_BLOCKS_SOKOGEN_28,
      },
    },
    currentBlocks: {
      left: JSON.parse(JSON.stringify(INITIAL_BLOCKS_TUTORIAL_1)),
      front: JSON.parse(JSON.stringify(INITIAL_BLOCKS_SOKOGEN_4_ROTATE_270)),
      top: JSON.parse(JSON.stringify(INITIAL_BLOCKS_SOKOGEN_11)),
    },
    currentMarmitronPositions: {
      left: {
        x: 3,
        y: 3,
        exist: true,
      },
      front: {
        x: 0,
        y: 0,
        exist: false,
      },
      top: {
        x: 0,
        y: 0,
        exist: false,
      },
    },
    currentFace: 'left',
    currentLevel: 0,
    rows: 7,
    cols: 7,
    queuedMove: null,
    moveLock: false,
    animationLock: false,
    success: false,
  },
  mutations: {
    moveUnlock(state) {
      state.moveLock = false
    },
    animationUnlock(state) {
      state.animationLock = false
    },
    setDifficulty(state, difficulty) {
      if (["easy", "normal", "hard"].includes(difficulty)) {
        if (!state.lockDifficulty) {
          state.difficulty = difficulty
        }
      }
    },
    lockDifficulty(state) {
      state.lockDifficulty = true
    },
    checkQueuedMove(state) {
      state.moveLock = false
      let queuedMove = state.queuedMove
      state.queuedMove = null

      if (["left", "right", "up", "down"].includes(queuedMove)) {
        store.commit('move', queuedMove)
      }
    },
    move(state, direction) {
      if (state.animationLock) {
        return
      }

      if (state.moveLock) {
        state.queuedMove = direction

        return
      }

      state.moveLock = true

      setTimeout(store.commit, 400, "checkQueuedMove")

      if (["left", "right", "up", "down"].includes(direction)) {
        // The first move locks difficulty to ensure the map will not be changed during a game
        state.lockDifficulty = true
      }

      if (direction === "left") {
        let xAfterLeft = state.currentMarmitronPositions[state.currentFace].x - 1
        if (!isWalkableAt(xAfterLeft, state.currentMarmitronPositions[state.currentFace].y, "left", true)) {
          return
        } else {
          state.currentMarmitronPositions[state.currentFace].x = xAfterLeft
          moveBlockIfExist(
            state.currentMarmitronPositions[state.currentFace].x, state.currentMarmitronPositions[state.currentFace].y,
            state.currentMarmitronPositions[state.currentFace].x - 1, state.currentMarmitronPositions[state.currentFace].y,
          )
        }
      } else if (direction === "right") {
        let xAfterRight = state.currentMarmitronPositions[state.currentFace].x + 1
        if (!isWalkableAt(xAfterRight, state.currentMarmitronPositions[state.currentFace].y, "right", true)) {
          return
        } else {
          state.currentMarmitronPositions[state.currentFace].x = xAfterRight
          moveBlockIfExist(
            state.currentMarmitronPositions[state.currentFace].x, state.currentMarmitronPositions[state.currentFace].y,
            state.currentMarmitronPositions[state.currentFace].x + 1, state.currentMarmitronPositions[state.currentFace].y,
          )
        }
      } else if (direction === "up") {
        let yAfterUp = state.currentMarmitronPositions[state.currentFace].y - 1
        if (!isWalkableAt(state.currentMarmitronPositions[state.currentFace].x, yAfterUp, "up", true)) {
          return
        } else {
          state.currentMarmitronPositions[state.currentFace].y = yAfterUp
          moveBlockIfExist(
            state.currentMarmitronPositions[state.currentFace].x, state.currentMarmitronPositions[state.currentFace].y,
            state.currentMarmitronPositions[state.currentFace].x, state.currentMarmitronPositions[state.currentFace].y - 1,
          )
        }
      } else if (direction === "down") {
        let yAfterDown = state.currentMarmitronPositions[state.currentFace].y + 1
        if (!isWalkableAt(state.currentMarmitronPositions[state.currentFace].x, yAfterDown, "down", true)) {
          return
        } else {
          state.currentMarmitronPositions[state.currentFace].y = yAfterDown
          moveBlockIfExist(
            state.currentMarmitronPositions[state.currentFace].x, state.currentMarmitronPositions[state.currentFace].y,
            state.currentMarmitronPositions[state.currentFace].x, state.currentMarmitronPositions[state.currentFace].y + 1,
          )
        }
      }

      if (state.currentLevel === 0) {
        if (checkSuccess("left")) {
          state.animationLock = true
          setTimeout(store.commit, 1000, "setCurrentLevel", 1)
        }
      } else if (state.currentLevel === 1) {
        if (checkSuccess("front")) {
          state.animationLock = true
          setTimeout(store.commit, 1000, "setCurrentLevel", 2)
        }
      } else if (state.currentLevel === 2 && state.success === false) {
        if (checkSuccess("top")) {
          state.animationLock = true
          setTimeout(store.commit, 1000, "success")
        }
      }

      store.commit('checkPassage')
    },
    setCurrentLevel(state, level) {
      if (state.currentLevel < level) {
        state.animationLock = false
        state.currentLevel = level
      }
    },
    success(state) {
      if (state.success === false) {
        state.animationLock = false
        state.success = true
      }
    },
    checkPassage(state) {
      let marmitronX = state.currentMarmitronPositions[state.currentFace].x
      let marmitronY = state.currentMarmitronPositions[state.currentFace].y

      if (state.grids[state.difficulty][state.currentFace][marmitronY][marmitronX] === 'R') {
        state.animationLock = true

        let passageDestinationPosition = getSpecialPosition('front', 'L')
        state.currentMarmitronPositions.front.x = passageDestinationPosition.x
        state.currentMarmitronPositions.front.y = passageDestinationPosition.y
        state.currentMarmitronPositions.front.exist = true

        setTimeout(store.commit, 400, "setFace", 'front')
      } else if (state.grids[state.difficulty][state.currentFace][marmitronY][marmitronX] === 'L') {
        state.animationLock = true

        let passageDestinationPosition = getSpecialPosition('left', 'R')
        state.currentMarmitronPositions.left.x = passageDestinationPosition.x
        state.currentMarmitronPositions.left.y = passageDestinationPosition.y
        state.currentMarmitronPositions.left.exist = true

        setTimeout(store.commit, 400, "setFace", 'left')
      } else if (state.grids[state.difficulty][state.currentFace][marmitronY][marmitronX] === 'U') {
        state.animationLock = true

        let passageDestinationPosition = getSpecialPosition('top', 'D')
        state.currentMarmitronPositions.top.x = passageDestinationPosition.x
        state.currentMarmitronPositions.top.y = passageDestinationPosition.y
        state.currentMarmitronPositions.top.exist = true

        setTimeout(store.commit, 400, "setFace", 'top')
      } else if (state.grids[state.difficulty][state.currentFace][marmitronY][marmitronX] === 'D') {
        state.animationLock = true

        let passageDestinationPosition = getSpecialPosition('front', 'U')
        state.currentMarmitronPositions.front.x = passageDestinationPosition.x
        state.currentMarmitronPositions.front.y = passageDestinationPosition.y
        state.currentMarmitronPositions.front.exist = true

        setTimeout(store.commit, 400, "setFace", 'front')
      }
    },
    setFace(state, face) {
      let originFace = state.currentFace
      state.currentMarmitronPositions[originFace].exist = false

      state.currentFace = face

      setTimeout(store.commit, 800, "moveMarmitronOutOfPassage", originFace)
    },
    moveMarmitronOutOfPassage(state, originFace) {
      if (state.currentFace === 'left') {
        state.currentMarmitronPositions[state.currentFace].x--
      } else if (originFace === 'left' && state.currentFace === 'front') {
        state.currentMarmitronPositions[state.currentFace].x++
      } else if (originFace === 'top' && state.currentFace === 'front') {
        state.currentMarmitronPositions[state.currentFace].y++
      } else if (state.currentFace === 'top') {
        state.currentMarmitronPositions[state.currentFace].y--
      }

      setTimeout(store.commit, 400, "animationUnlock")
    },
    reset(state) {
      if (state.currentFace === 'left' && state.currentLevel >= 1) {
        return
      } else if (state.currentFace === 'front' && state.currentLevel >= 2) {
        return
      } else if (state.currentFace === 'top' && state.success) {
        return
      }

      for (var i = 0 ; i < state.initialBlocks[state.difficulty][state.currentFace].length ; i++) {
        state.currentBlocks[state.currentFace][i].x = state.initialBlocks[state.difficulty][state.currentFace][i].x
        state.currentBlocks[state.currentFace][i].y = state.initialBlocks[state.difficulty][state.currentFace][i].y
      }

      if (state.currentFace === 'front') {
        let initialFrontPosition = getSpecialPosition(state.currentFace, 'L')

        state.currentMarmitronPositions[state.currentFace].x = initialFrontPosition.x + 1
        state.currentMarmitronPositions[state.currentFace].y = initialFrontPosition.y
      } else {
        // Current face is top, because reset is not allowed during the first grid
        let initialFrontPosition = getSpecialPosition(state.currentFace, 'D')

        state.currentMarmitronPositions[state.currentFace].x = initialFrontPosition.x
        state.currentMarmitronPositions[state.currentFace].y = initialFrontPosition.y - 1
      }
    },
  },
})

function getSpecialPosition(face, passage) {
  for (var i = 0 ; i < store.state.grids[store.state.difficulty][face].length ; i++) {
    for (var j = 0 ; j < store.state.grids[store.state.difficulty][face][i].length ; j++) {
      if (store.state.grids[store.state.difficulty][face][i][j] === passage) {
        return {x: j, y: i}
      }
    }
  }

  // Fallback, but not supposed to happen
  return {x: 1, y: 1}
}

function isWalkableAt(x, y, direction, walkablePassages) {
  if (!(0 <= x && x < store.state.rows)) {
    return false
  }

  if (!(0 <= y && y < store.state.cols)) {
    return false
  }

  let cellContent = store.state.grids[store.state.difficulty][store.state.currentFace][y][x]

  if (cellContent === 'W') {
    return false
  }

  if (cellContent === 'R') {
    return walkablePassages && store.state.currentLevel >= 1
  } else if (cellContent === 'U') {
    return walkablePassages && store.state.currentLevel >= 2
  } else if (cellContent === 'L' || cellContent === 'D') {
    return walkablePassages
  }

  for (var block of store.state.currentBlocks[store.state.currentFace]) {
    if (block.x === x && block.y === y) {
      if (store.state.currentFace === 'left' && store.state.currentLevel >= 1) {
        return false
      } else if (store.state.currentFace === 'front' && store.state.currentLevel >= 2) {
        return false
      } else if (store.state.currentFace === 'top' && store.state.success) {
        return false
      }

      if (direction === 'left') {
        return isWalkableAt(x - 1, y, null, false)
      } else if (direction === 'right') {
        return isWalkableAt(x + 1, y, null, false)
      } else if (direction === 'up') {
        return isWalkableAt(x, y - 1, null, false)
      } else if (direction === 'down') {
        return isWalkableAt(x, y + 1, null, false)
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

function checkSuccess(face) {
  for (var block of store.state.currentBlocks[face]) {
    if (!['0', '1', '2', '3', '4', '5', '6', '7'].includes(store.state.grids[store.state.difficulty][store.state.currentFace][block.y][block.x])) {
      return false
    }
  }

  return true
}

export default store
