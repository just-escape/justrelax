import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

const cornerTopLeft = {
  type: 'wall',
  texture: require('@/assets/img/corner-top-left.png'),
}

const cornerTopRight = {
  type: 'wall',
  texture: require('@/assets/img/corner-top-right.png'),
}

const cornerBottomRight = {
  type: 'wall',
  texture: require('@/assets/img/corner-bottom-right.png'),
}

const cornerBottomLeft = {
  type: 'wall',
  texture: require('@/assets/img/corner-bottom-left.png'),
}

const angleTopLeft = {
  type: 'wall',
  texture: require('@/assets/img/angle-top-left.png'),
}

const angleTopRight = {
  type: 'wall',
  texture: require('@/assets/img/angle-top-right.png'),
}

const angleBottomRight = {
  type: 'wall',
  texture: require('@/assets/img/angle-bottom-right.png'),
}

const angleBottomLeft = {
  type: 'wall',
  texture: require('@/assets/img/angle-bottom-left.png'),
}

const wallTop = {
  type: 'wall',
  texture: require('@/assets/img/wall-top.png'),
}

const wallLeft = {
  type: 'wall',
  texture: require('@/assets/img/wall-left.png'),
}

const wallRight = {
  type: 'wall',
  texture: require('@/assets/img/wall-right.png'),
}

const wallBottom = {
  type: 'wall',
  texture: require('@/assets/img/wall-bottom.png'),
}

const gateTop = {
  type: 'gate-top',
  texture: require('@/assets/img/gate-top.png'),
  animatedTextureFast: require('@/assets/img/gate-top-fast.gif'),
  animatedTextureSlow: require('@/assets/img/gate-top-slow.gif'),
  floorTexture: require('@/assets/img/floor.png'),
}

const gateLeft = {
  type: 'gate-left',
  texture: require('@/assets/img/gate-left.png'),
  animatedTextureFast: require('@/assets/img/gate-left-fast.gif'),
  animatedTextureSlow: require('@/assets/img/gate-left-slow.gif'),
  floorTexture: require('@/assets/img/floor.png'),
}

const gateRight = {
  type: 'gate-right',
  texture: require('@/assets/img/gate-right.png'),
  animatedTextureFast: require('@/assets/img/gate-right-fast.gif'),
  animatedTextureSlow: require('@/assets/img/gate-right-slow.gif'),
  floorTexture: require('@/assets/img/floor.png'),
}

const gateBottom = {
  type: 'gate-bottom',
  texture: require('@/assets/img/gate-bottom.png'),
  animatedTextureFast: require('@/assets/img/gate-bottom-fast.gif'),
  animatedTextureSlow: require('@/assets/img/gate-bottom-slow.gif'),
  floorTexture: require('@/assets/img/floor.png'),
}

const column = {
  type: 'wall',
  texture: require('@/assets/img/column.png'),
}

const wall = {
  type: 'wall',
  texture: require('@/assets/img/wall.png'),
}

const floor = {
  type: 'floor',
  texture: require('@/assets/img/floor.png'),
}

const chamber1 = {
  type: 'chamber',
  id: 1,
  texture: require('@/assets/img/chamber.png'),
  successTexture: require('@/assets/img/chamber-1.gif'),
  foodTexture: require('@/assets/img/potatoe.png'),
}

const chamber2 = {
  type: 'chamber',
  id: 2,
  texture: require('@/assets/img/chamber.png'),
  successTexture: require('@/assets/img/chamber-2.gif'),
  foodTexture: require('@/assets/img/cinnamon.png'),
}

const chamber3 = {
  type: 'chamber',
  id: 3,
  texture: require('@/assets/img/chamber.png'),
  successTexture: require('@/assets/img/chamber-3.gif'),
  foodTexture: require('@/assets/img/lemon.png'),
}

const chamber4 = {
  type: 'chamber',
  id: 4,
  texture: require('@/assets/img/chamber.png'),
  successTexture: require('@/assets/img/chamber-4.gif'),
  foodTexture: require('@/assets/img/mint.png'),
}

const chamber5 = {
  type: 'chamber',
  id: 5,
  texture: require('@/assets/img/chamber.png'),
  successTexture: require('@/assets/img/chamber-5.gif'),
  foodTexture: require('@/assets/img/insect.png'),
}

const chamber6 = {
  type: 'chamber',
  id: 6,
  texture: require('@/assets/img/chamber.png'),
  successTexture: require('@/assets/img/chamber-6.gif'),
  foodTexture: require('@/assets/img/algua.png'),
}

const chamber7 = {
  type: 'chamber',
  id: 7,
  texture: require('@/assets/img/chamber.png'),
  successTexture: require('@/assets/img/chamber-7.gif'),
  foodTexture: require('@/assets/img/chocoffee.png'),
}

const chamber8 = {
  type: 'chamber',
  id: 8,
  texture: require('@/assets/img/chamber.png'),
  successTexture: require('@/assets/img/chamber-8.gif'),
  foodTexture: require('@/assets/img/beer.png'),
}

const INITIAL_GRID_TUTORIAL_1 = [
  [wall,              wall,               cornerTopLeft,      wallTop,      wallTop,            wallTop,      cornerTopRight],
  [wall,              wall,               wallLeft,           floor,        floor,              floor,        gateRight],
  [cornerTopLeft,     wallTop,            angleTopLeft,       floor,        column,             floor,        wallRight],
  [wallLeft,          chamber3,           floor,              floor,        floor,              floor,        wallRight],
  [cornerBottomLeft,  angleBottomLeft,    floor,              floor,        angleBottomRight,   wallBottom,   cornerBottomRight],
  [wall,              cornerBottomLeft,   angleBottomLeft,    chamber5,     wallRight,          wall,         wall],
  [wall,              wall,               cornerBottomLeft,   wallBottom,   cornerBottomRight,  wall,         wall],
]

const INITIAL_BLOCKS_TUTORIAL_1 = [
  {
    x: 2,
    y: 3,
  },
  {
    x: 3,
    y: 4,
  },
]

const INITIAL_GRID_TUTORIAL_1_LOWER_PASSAGE = [
  [wall,              wall,               cornerTopLeft,      wallTop,      wallTop,            wallTop,      cornerTopRight],
  [wall,              wall,               wallLeft,           floor,        floor,              floor,        wallRight],
  [cornerTopLeft,     wallTop,            angleTopLeft,       floor,        column,             floor,        wallRight],
  [wallLeft,          chamber3,           floor,              floor,        floor,              floor,        gateRight],
  [cornerBottomLeft,  angleBottomLeft,    floor,              floor,        angleBottomRight,   wallBottom,   cornerBottomRight],
  [wall,              cornerBottomLeft,   angleBottomLeft,    chamber5,     wallRight,          wall,         wall],
  [wall,              wall,               cornerBottomLeft,   wallBottom,   cornerBottomRight,  wall,         wall],
]

const INITIAL_GRID_TUTORIAL_2 = [
  [cornerTopLeft,     wallTop,      wallTop,      gateTop,      wallTop,      wallTop,      cornerTopRight],
  [gateLeft,          floor,        floor,        floor,        floor,        floor,        wallRight],
  [wallLeft,          floor,        floor,        column,       chamber6,     floor,        wallRight],
  [wallLeft,          floor,        floor,        chamber4,     floor,        floor,        wallRight],
  [wallLeft,          floor,        chamber1,     column,       floor,        floor,        wallRight],
  [wallLeft,          floor,        floor,        floor,        floor,        floor,        wallRight],
  [cornerBottomLeft,  wallBottom,   wallBottom,   wallBottom,   wallBottom,   wallBottom,   cornerBottomRight],
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
  [wall,              cornerTopLeft,      wallTop,      wallTop,      wallTop,      cornerTopRight,     wall],
  [cornerTopLeft,     angleTopLeft,       floor,        chamber8,     floor,        angleTopRight,      cornerTopRight],
  [wallLeft,          floor,              floor,        chamber2,     floor,        floor,              wallRight],
  [wallLeft,          floor,              floor,        chamber7,     floor,        floor,              wallRight],
  [wallLeft,          floor,              floor,        column,       floor,        floor,              wallRight],
  [cornerBottomLeft,  angleBottomLeft,    floor,        floor,        floor,        angleBottomRight,   cornerBottomRight],
  [wall,              cornerBottomLeft,   wallBottom,   gateBottom,   wallBottom,   cornerBottomRight,  wall],
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
  [wall,              cornerTopLeft,    wallTop,      gateTop,      wallTop,      cornerTopRight,     wall],
  [cornerTopLeft,     angleTopLeft,     floor,        floor,        floor,        angleTopRight,      cornerTopRight],
  [wallLeft,          floor,            floor,        floor,        floor,        floor,              wallRight],
  [gateLeft,          floor,            column,       chamber1,     chamber6,     chamber4,           wallRight],
  [wallLeft,          floor,            floor,        floor,        floor,        floor,              wallRight],
  [cornerBottomLeft,  angleBottomLeft,  floor,        floor,        floor,        angleBottomRight,   cornerBottomRight],
  [wall,              cornerBottomLeft, wallBottom,   wallBottom,   wallBottom,   cornerBottomRight,  wall],
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
  [cornerTopLeft,     wallTop,    wallTop,      wallTop,      cornerTopRight,   wall,       wall],
  [wallLeft,          floor,      floor,        floor,        wallRight,        wall,       wall],
  [wallLeft,          floor,      column,       floor,        angleTopRight,    wallTop,    cornerTopRight],
  [wallLeft,          chamber7,   chamber2,     floor,        floor,            floor,      wallRight],
  [wallLeft,          floor,      floor,        column,       floor,            floor,      wallRight],
  [wallLeft,          floor,      floor,        floor,        floor,            chamber8,   wallRight],
  [cornerBottomLeft,  wallBottom, wallBottom,   gateBottom,   wallBottom,       wallBottom, cornerBottomRight],
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
  [cornerTopLeft,     wallTop,    wallTop,      wallTop,      gateTop,            wallTop,      cornerTopRight],
  [gateLeft,          floor,      floor,        floor,        floor,              chamber4,     wallRight],
  [wallLeft,          floor,      floor,        column,       floor,              floor,        wallRight],
  [wallLeft,          chamber1,   chamber6,     floor,        floor,              floor,        wallRight],
  [wallLeft,          floor,      column,       floor,        angleBottomRight,   wallBottom,   cornerBottomRight],
  [wallLeft,          floor,      floor,        floor,        wallRight,          wall,         wall],
  [cornerBottomLeft,  wallBottom, wallBottom,   wallBottom,   cornerBottomRight,  wall,         wall],
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
  [cornerTopLeft,     wallTop,    wallTop,      wallTop,      cornerTopRight,   wall,       wall],
  [wallLeft,          floor,      floor,        floor,        wallRight,        wall,       wall],
  [wallLeft,          floor,      column,       floor,        angleTopRight,    wallTop,    cornerTopRight],
  [wallLeft,          chamber8,   floor,        floor,        floor,            floor,      wallRight],
  [wallLeft,          chamber2,   floor,        floor,        column,           floor,      wallRight],
  [wallLeft,          floor,      floor,        chamber7,     floor,            floor,      wallRight],
  [cornerBottomLeft,  wallBottom, wallBottom,   wallBottom,   gateBottom,       wallBottom, cornerBottomRight],
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
    faceAnimationFlags: {
      left: [],
      front: [],
      top: [],
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
          if (state.difficulty === 'easy') {
            state.currentBlocks = {
              left: JSON.parse(JSON.stringify(INITIAL_BLOCKS_TUTORIAL_1)),
              front: JSON.parse(JSON.stringify(INITIAL_BLOCKS_TUTORIAL_2)),
              top: JSON.parse(JSON.stringify(INITIAL_BLOCKS_SOKOGEN_4_ROTATE_180)),
            }
          } else if (state.difficulty === 'normal') {
            state.currentBlocks = {
              left: JSON.parse(JSON.stringify(INITIAL_BLOCKS_TUTORIAL_1)),
              front: JSON.parse(JSON.stringify(INITIAL_BLOCKS_SOKOGEN_4_ROTATE_270)),
              top: JSON.parse(JSON.stringify(INITIAL_BLOCKS_SOKOGEN_11)),
            }
          } else if (state.difficulty === 'hard') {
            state.currentBlocks = {
              left: JSON.parse(JSON.stringify(INITIAL_BLOCKS_TUTORIAL_1)),
              front: JSON.parse(JSON.stringify(INITIAL_BLOCKS_SOKOGEN_11_UPSIDE_DOWN)),
              top: JSON.parse(JSON.stringify(INITIAL_BLOCKS_SOKOGEN_11)),
            }
          }
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
    control(state, {name, pressed}) {
      if (pressed) {
        if (name === 'reset') {
          store.commit('reset')
        } else if (["left", "right", "up", "down"].includes(name)) {
          store.commit('move', name)
        }
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
          setTimeout(store.commit, 1000, "addFaceAnimationFlag", {face: "left", flag: "turnCylinders"})
          setTimeout(store.commit, 3000, "addFaceAnimationFlag", {face: "left", flag: "displayFood"})
          setTimeout(store.commit, 4500, "addFaceAnimationFlag", {face: "left", flag: "displayChamberIds"})
          setTimeout(store.commit, 5500, "addFaceAnimationFlag", {face: "left", flag: "activateGates"})
          setTimeout(store.commit, 5500, "setCurrentLevel", 1)
        }
      } else if (state.currentLevel === 1) {
        if (checkSuccess("front")) {
          state.animationLock = true
          setTimeout(store.commit, 1000, "addFaceAnimationFlag", {face: "front", flag: "turnCylinders"})
          setTimeout(store.commit, 3000, "addFaceAnimationFlag", {face: "front", flag: "displayFood"})
          setTimeout(store.commit, 4500, "addFaceAnimationFlag", {face: "front", flag: "displayChamberIds"})
          setTimeout(store.commit, 5500, "addFaceAnimationFlag", {face: "front", flag: "activateGates"})
          setTimeout(store.commit, 5500, "setCurrentLevel", 2)
        }
      } else if (state.currentLevel === 2 && state.success === false) {
        if (checkSuccess("top")) {
          state.animationLock = true
          setTimeout(store.commit, 1000, "addFaceAnimationFlag", {face: "top", flag: "turnCylinders"})
          setTimeout(store.commit, 3000, "addFaceAnimationFlag", {face: "top", flag: "displayFood"})
          setTimeout(store.commit, 4500, "addFaceAnimationFlag", {face: "top", flag: "displayChamberIds"})
          setTimeout(store.commit, 5500, "success")
        }
      }

      store.commit('checkPassage')
    },
    setCurrentLevel(state, level) {
      if (state.currentLevel < level) {
        state.currentLevel = level
        state.animationLock = false
      }
    },
    addFaceAnimationFlag(state, {face, flag}) {
      state.faceAnimationFlags[face].push(flag)
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

      if (state.grids[state.difficulty][state.currentFace][marmitronY][marmitronX].type === 'gate-right') {
        state.animationLock = true

        let passageDestinationPosition = getSpecialPosition('front', 'gate-left')
        state.currentMarmitronPositions.front.x = passageDestinationPosition.x
        state.currentMarmitronPositions.front.y = passageDestinationPosition.y
        state.currentMarmitronPositions.front.exist = true

        setTimeout(store.commit, 400, "setFace", 'front')
      } else if (state.grids[state.difficulty][state.currentFace][marmitronY][marmitronX].type === 'gate-left') {
        state.animationLock = true

        let passageDestinationPosition = getSpecialPosition('left', 'gate-right')
        state.currentMarmitronPositions.left.x = passageDestinationPosition.x
        state.currentMarmitronPositions.left.y = passageDestinationPosition.y
        state.currentMarmitronPositions.left.exist = true

        setTimeout(store.commit, 400, "setFace", 'left')
      } else if (state.grids[state.difficulty][state.currentFace][marmitronY][marmitronX].type === 'gate-top') {
        state.animationLock = true

        let passageDestinationPosition = getSpecialPosition('top', 'gate-bottom')
        state.currentMarmitronPositions.top.x = passageDestinationPosition.x
        state.currentMarmitronPositions.top.y = passageDestinationPosition.y
        state.currentMarmitronPositions.top.exist = true

        setTimeout(store.commit, 400, "setFace", 'top')
      } else if (state.grids[state.difficulty][state.currentFace][marmitronY][marmitronX].type === 'gate-bottom') {
        state.animationLock = true

        let passageDestinationPosition = getSpecialPosition('front', 'gate-top')
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
      if (state.animationLock === true) {
        return
      }

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

      if (state.currentFace === 'left') {
        // The first grid is the same for all difficulty levels
        state.currentMarmitronPositions[state.currentFace].x = 3
        state.currentMarmitronPositions[state.currentFace].y = 3
      } else if (state.currentFace === 'front') {
        let initialFrontPosition = getSpecialPosition(state.currentFace, 'gate-left')

        state.currentMarmitronPositions[state.currentFace].x = initialFrontPosition.x + 1
        state.currentMarmitronPositions[state.currentFace].y = initialFrontPosition.y
      } else {
        // Current face is top
        let initialFrontPosition = getSpecialPosition(state.currentFace, 'gate-bottom')

        state.currentMarmitronPositions[state.currentFace].x = initialFrontPosition.x
        state.currentMarmitronPositions[state.currentFace].y = initialFrontPosition.y - 1
      }
    },
  },
})

function getSpecialPosition(face, passage) {
  for (var i = 0 ; i < store.state.grids[store.state.difficulty][face].length ; i++) {
    for (var j = 0 ; j < store.state.grids[store.state.difficulty][face][i].length ; j++) {
      if (store.state.grids[store.state.difficulty][face][i][j].type === passage) {
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

  let cellType = store.state.grids[store.state.difficulty][store.state.currentFace][y][x].type

  if (cellType === 'wall') {
    return false
  }

  if (cellType === 'gate-right') {
    return walkablePassages && store.state.currentLevel >= 1
  } else if (cellType === 'gate-top') {
    return walkablePassages && store.state.currentLevel >= 2
  } else if (cellType === 'gate-left' || cellType === 'gate-bottom') {
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
    if (store.state.grids[store.state.difficulty][store.state.currentFace][block.y][block.x].type != 'chamber') {
      return false
    }
  }

  return true
}

export default store
