import Vue from 'vue'
import Vuex from 'vuex'

import difficultyStore from '@/store/difficultyStore.js'
import progressionStore from '@/store/progressionStore.js'
import publishSubscribeService from './publishSubscribeService'
import lightLogStore from '@/store/lightLogStore.js'

Vue.use(Vuex)


const ACTIVATION_SEQUENCE_EASY = [
  '31-32',
  '32-33',
  '33-24',
  '24-25',
  '25-26',
]

const ACTIVATION_SEQUENCE_NORMAL_AND_HARD_1 = [
  '51-52',
  '52-43',
  '43-32',
  '32-23',
  '23-24',
  '24-34',
  '34-35',
]

const ACTIVATION_SEQUENCE_HARD_2 = [
  '11-12',
  '12-23',
  '32-23',
  '43-32',
  '43-44',
  '44-34',
  '34-35',
]

function setPlayable() {
  store.commit('setPlayable')
}

function verticesToTurquoise(verticeIds) {
  store.commit('setVerticesTransparent')

  var i

  var targetR = 0
  var targetG = 209
  var targetB = 182
  var targetAs = []
  for (i = 0 ; i < verticeIds.length ; i++) {
    var pseudoRandom = Math.sin(i) * 10000  // Almost random, but deterministic
    pseudoRandom -= Math.floor(pseudoRandom)
    targetAs.push(pseudoRandom * 0.4 + 0.3)
  }

  Vue.prototype.$anime({
    duration: 8000,
    easing: 'easeInQuad',
    update(anim) {
      for (i = 0 ; i < verticeIds.length ; i++) {
        var verticeId = verticeIds[i]
        if (!store.state.vertices[verticeId].startingPoint) {
          var r = store.state.vertices[verticeId].initColor.r - (store.state.vertices[verticeId].initColor.r - targetR) * anim.progress / 100
          var g = store.state.vertices[verticeId].initColor.g - (store.state.vertices[verticeId].initColor.g - targetG) * anim.progress / 100
          var b = store.state.vertices[verticeId].initColor.b - (store.state.vertices[verticeId].initColor.b - targetB) * anim.progress / 100
          var a = store.state.vertices[verticeId].initColor.a - (store.state.vertices[verticeId].initColor.a - targetAs[i]) * anim.progress / 100
          store.commit('setVerticeRGBA', {verticeId, r, g, b, a})
        }
      }

      var colorValidatedR = 255 - 255 * anim.progress / 100
      var colorValidatedG = 255 - (255 - 209) * anim.progress / 100
      var colorValidatedB = 255 - (255 - 182) * anim.progress / 100
      var colorValidatedA = 1 - 0.6 * anim.progress / 100
      store.state.colorValidated = 'rgba(' + colorValidatedR + ', ' + colorValidatedG + ', ' + colorValidatedB + ', ' + colorValidatedA + ')'
    }
  })
}

function activateEdgesForFinalAnimation(edgeIds) {
  Vue.prototype.$anime.timeline({
    easing: 'linear',
    begin: function() {
      for (var i = 0 ; i < edgeIds.length ; i++) {
        store.commit('setEdgeFinalAnimation', edgeIds[i])

        var verticeId = store.state.edges[edgeIds[i]].getVertice2()
        var glow = 'glowing-transition'
        store.commit('setVerticeGlow', {verticeId, glow})
      }
    },
    complete: function() {
      for (var i = 0 ; i < edgeIds.length ; i++) {
        store.commit('validateEdge', edgeIds[i])

        var verticeId = store.state.edges[edgeIds[i]].getVertice2()
        var glow = 'glowing-more'
        store.commit('setVerticeGlow', {verticeId, glow})
      }

      propagateFinalAnimation()
    },
  })
  .add({
    duration: 2000,
    targets: '.gradientColor1',
    offset: '75%',
  })
  .add({
    duration: 2000,
    targets: '.gradientColor2',
    offset: '85%',
  }, '-=2000')
  .add({
    duration: 1500,
    targets: '#glowing-transition-intensity',
    stdDeviation: "12",
  }, '-=1500')
  .add({
    duration: 1,
    targets: '.gradientColor1',
    offset: '0%',
  })
  .add({
    duration: 1,
    targets: '.gradientColor2',
    offset: '10%',
  }, '-=1')
  .add({
    duration: 1,
    targets: '#glowing-transition-intensity',
    stdDeviation: "1.7",
  }, '-=1')
}

function propagateFinalAnimation() {
  var edgeIds = store.getters.nextFinalAnimationEdgeIds

  if (edgeIds.length == 0) {
    setTimeout(verticesToTurquoise, 1000, Object.keys(store.state.vertices))
  } else {
    var verticeIds = []
    for (var i = 0 ; i < edgeIds.length ; i++) {
      verticeIds.push(store.state.edges[edgeIds[i]].getVertice2())
    }

    activateEdgesForFinalAnimation(edgeIds)
  }
}

function activateEdge(edgeId) {
  var verticeId = store.state.edges[edgeId].getVertice2()

  var activationAnimation = Vue.prototype.$anime.timeline({
    easing: 'linear',
    begin: function() {
      store.commit('activateEdge', edgeId)
      var glow = 'glowing-transition'
      store.commit('setVerticeGlow', {verticeId, glow})
      store.commit('startVerticePulse', verticeId)
    },
    complete: function() {
      store.commit('validateEdge', edgeId)
      var glow = 'glowing-more'
      store.commit('setVerticeGlow', {verticeId, glow})
      store.commit('stopVerticePulse', verticeId)
      nextActivation()
    },
  })
  .add({
    duration: 5000,
    targets: '.gradientColor1',
    offset: '75%',
  })
  .add({
    duration: 5000,
    targets: '.gradientColor2',
    offset: '85%',
  }, '-=5000')
  .add({
    duration: 5000,
    targets: '#glowing-transition-intensity',
    stdDeviation: "12",
  }, '-=5000')
  .add({
    duration: 1,
    targets: '.gradientColor1',
    offset: '0%',
  })
  .add({
    duration: 1,
    targets: '.gradientColor2',
    offset: '10%',
  }, '-=1')
  .add({
    duration: 1,
    targets: '#glowing-transition-intensity',
    stdDeviation: "1.7",
  }, '-=1')

  store.commit('setActivationAnimation', activationAnimation)
}

function nextActivation() {
  var edgeId = store.getters.currentActivationEdgeId

  // The end of the activation sequence has been reached
  if (edgeId === null) {
    store.commit('setUnplayable')
    confirmationAnimation()
  } else {
    let currentSensorId = store.state.vertices[store.state.edges[edgeId].getVertice1()].activationSensorId
    let nextSensorId = store.state.vertices[store.state.edges[edgeId].getVertice2()].activationSensorId
    if (store.state.activatedSensors.slice(0, 4).includes(nextSensorId)) {
      if (currentSensorId) {
        // Not the first vertice of the sequence
        store.commit('hideColorTriangles', currentSensorId)
      } else {
        // The first vertice of the sequence
        store.commit('showColorTriangles', nextSensorId)
      }

      let nextEdgeId = store.getters.nextActivationEdgeId
      if (nextEdgeId) {
        // This is not the final edge
        store.commit('anticipateNextActivation', store.state.vertices[store.state.edges[nextEdgeId].getVertice2()])
      }

      activateEdge(edgeId)
    } else {
      if (store.state.currentActivationSequence[1] == edgeId) {
        gameOver(setPlayable, true)
      } else {
        gameOver(newActivationSequence, true)
        if (nextSensorId === "pink") {
          store.dispatch("recordGameOver", "pink_not_on")
        } else {
          store.dispatch("recordGameOver", "next_light_not_on")
        }
      }
    }
  }
}

function confirmationAnimation() {
  var timeout = 500

  for (var color in store.state.colorTriangles) {
    store.commit('hideColorTriangles', color)
  }

  for (var i = 0 ; i < store.state.currentActivationSequence.length ; i++) {
    var verticeId = store.state.edges[store.state.currentActivationSequence[i]].getVertice2()
    setTimeout(store.commit, timeout, 'startVerticePulse', verticeId)
    setTimeout(store.commit, timeout + 300, 'stopVerticePulse', verticeId)
    timeout += 400
  }

  timeout += 400
  setTimeout(propagateFinalAnimation, timeout)

  progressionStore.commit("setLightServiceSuccess")
}

function _deactivateEdge(edgeId, callback) {
  var verticeId = store.state.edges[edgeId].getVertice2()

  Vue.prototype.$anime.timeline({
    easing: 'linear',
    begin: function() {
      store.commit('invalidateEdge', edgeId)
      var glow = 'glowing-transition'
      store.commit('setVerticeGlow', {verticeId, glow})
    },
    complete: function() {
      store.commit('deactivateEdge', edgeId)
      var glow = 'glowing'
      store.commit('setVerticeGlow', {verticeId, glow})
      nextDeactivation(callback)
    },
  })
  .add({
    duration: 1000,
    targets: '.gradientColor1',
    offset: '0%',
  })
  .add({
    duration: 1000,
    targets: '.gradientColor2',
    offset: '10%',
  }, '-=1000')
  .add({
    duration: 1000,
    targets: '#glowing-transition-intensity',
    stdDeviation: "1.7",
  }, '-=1000')
}

function deactivateEdge(edgeId, callback) {
  /* If the deactivation sequence happens after an edge has been validated
   * and because conditions are not met to activate the next one, some
   * values have already been reset, so we need to preset them. Otherwise,
   * in the middle of the activation animation, values are already good ones.
   */
  if (store.state.edges[edgeId].validated) {
    Vue.prototype.$anime.timeline({
      complete: function() {
        _deactivateEdge(edgeId, callback)
      }
    })
    .add({
      duration: 1,
      targets: '.gradientColor1',
      offset: '75%',
    })
    .add({
      duration: 1,
      targets: '.gradientColor2',
      offset: '85%',
    }, '-=1')
    .add({
      duration: 1,
      targets: '#glowing-transition-intensity',
      stdDeviation: "12",
    }, '-=1')
  } else {
    _deactivateEdge(edgeId, callback)
  }
}

function nextDeactivation(callback) {
  var edgeId = store.getters.currentDeactivationEdgeId

  if (edgeId === null) {
    callback()
  } else {
    deactivateEdge(edgeId, callback)
  }
}

function newActivationPathEdge(i, edgeId) {
  Vue.prototype.$anime.timeline({
    easing: 'linear',
    begin: function() {
      store.commit('setEdgeActivationPathAnimation', edgeId)
    },
    complete: function() {
      var color = store.state.colorActivation
      store.commit('setEdgeColor', {edgeId, color})
      store.commit('unsetEdgeActivationPathAnimation', edgeId)
      _newActivationPath(i)
    },
  })
  .add({
    duration: 350,
    targets: '.gradientColor1',
    offset: '75%',
  })
  .add({
    duration: 350,
    targets: '.gradientColor2',
    offset: '85%',
  }, '-=350')
  .add({
    duration: 1,
    targets: '.gradientColor1',
    offset: '0%',
  })
  .add({
    duration: 1,
    targets: '.gradientColor2',
    offset: '10%',
  }, '-=1')
}

function _newActivationPath(i) {
  if (i < store.state.currentActivationSequence.length) {
    var edgeId = store.state.currentActivationSequence[i]
    newActivationPathEdge(i + 1, edgeId)
  } else {
    store.commit('setPlayable')
  }
}

function newActivationPath() {
  _newActivationPath(0)
}

function newActivationSequence() {
  store.commit('resetActivationSequenceEdgesColor')

  store.commit('loadNextActivationSequence')
  newActivationPath()
}

function gameOver(callback, blinkErrorAnimation) {
  store.commit('setUnplayable')

  for (var color in store.state.colorTriangles) {
    store.commit('hideColorTriangles', color)
  }
  store.commit('cancelNextActivationAnticipation')

  if (blinkErrorAnimation) {
    Vue.prototype.$anime.timeline({
      easing: 'linear',
      complete() {
        store.commit('hideGlobalError')
        nextDeactivation(callback)
      }
    })
    .add({
      duration: 500,
    })
    .add({
      duration: 1,
      update() {
        store.commit('showGlobalError')
      },
    })
    .add({
      duration: 150,
    })
    .add({
      duration: 1,
      update() {
        store.commit('hideGlobalError')
      }
    })
    .add({
      duration: 150,
    })
    .add({
      duration: 1,
      update() {
        store.commit('showGlobalError')
      },
    })
    .add({
      duration: 150,
    })
    .add({
      duration: 1,
      update() {
        store.commit('hideGlobalError')
      }
    })
    .add({
      duration: 500
    })
  } else {
    nextDeactivation(callback)
  }
}

var store = new Vuex.Store({
  state: {
    vertices: {
      '11': {
        x: 8 / 4 * 120 - 37.5,
        y: 0 / 2 * 60 * Math.sqrt(3) + 23,
        color: {
          r: 0,
          g: 209,
          b: 182,
          a: 0.7,
        },
        initColor: {
          r: 0,
          g: 209,
          b: 182,
          a: 0.7,
        },
        glowing: 'glowing',
        activationSensorId: null,
        startingPoint: true,
        pulse: false,
      },
      '12': {
        x: 10 / 4 * 120 - 37.5,
        y: 0 / 2 * 60 * Math.sqrt(3) + 23,
        color: {
          r: 253,
          g: 126,
          b: 20,
          a: 1,
        },
        initColor: {
          r: 253,
          g: 126,
          b: 20,
          a: 1,
        },
        glowing: 'glowing',
        activationSensorId: 'orange',
        startingPoint: false,
        pulse: false,
      },
      '13': {
        x: 12 / 4 * 120 - 37.5,
        y: 0 / 2 * 60 * Math.sqrt(3) + 23,
        color: {
          r: 255,
          g: 255,
          b: 255,
          a: 1,
        },
        initColor: {
          r: 255,
          g: 255,
          b: 255,
          a: 1,
        },
        glowing: 'glowing',
        activationSensorId: 'white',
        startingPoint: false,
        pulse: false,
      },
      '14': {
        x: 14 / 4 * 120 - 37.5,
        y: 0 / 2 * 60 * Math.sqrt(3) + 23,
        color: {
          r: 253,
          g: 126,
          b: 20,
          a: 1,
        },
        initColor: {
          r: 253,
          g: 126,
          b: 20,
          a: 1,
        },
        glowing: 'glowing',
        activationSensorId: 'orange',
        startingPoint: false,
        pulse: false,
      },
      '15': {
        x: 16 / 4 * 120 - 37.5,
        y: 0 / 2 * 60 * Math.sqrt(3) + 23,
        color: {
          r: 255,
          g: 255,
          b: 255,
          a: 1,
        },
        initColor: {
          r: 255,
          g: 255,
          b: 255,
          a: 1,
        },
        glowing: 'glowing',
        activationSensorId: 'white',
        startingPoint: false,
        pulse: false,
      },
      '21': {
        x: 7 / 4 * 120 - 37.5,
        y: 1 / 2 * 60 * Math.sqrt(3) + 23,
        color: {
          r: 0,
          g: 209,
          b: 182,
          a: 0.7,
        },
        initColor: {
          r: 0,
          g: 209,
          b: 182,
          a: 0.7,
        },
        glowing: 'glowing',
        activationSensorId: null,
        startingPoint: true,
        pulse: false,
      },
      '22': {
        x: 9 / 4 * 120 - 37.5,
        y: 1 / 2 * 60 * Math.sqrt(3) + 23,
        color: {
          r: 40,
          g: 167,
          b: 69,
          a: 1,
        },
        initColor: {
          r: 40,
          g: 167,
          b: 69,
          a: 1,
        },
        glowing: 'glowing',
        activationSensorId: 'green',
        startingPoint: false,
        pulse: false,
      },
      '23': {
        x: 11 / 4 * 120 - 37.5,
        y: 1 / 2 * 60 * Math.sqrt(3) + 23,
        color: {
          r: 0,
          g: 123,
          b: 255,
          a: 1,
        },
        initColor: {
          r: 0,
          g: 123,
          b: 255,
          a: 1,
        },
        glowing: 'glowing',
        activationSensorId: 'blue',
        startingPoint: false,
        pulse: false,
      },
      '24': {
        x: 13 / 4 * 120 - 37.5,
        y: 1 / 2 * 60 * Math.sqrt(3) + 23,
        color: {
          r: 220,
          g: 53,
          b: 69,
          a: 1,
        },
        initColor: {
          r: 220,
          g: 53,
          b: 69,
          a: 1,
        },
        glowing: 'glowing',
        activationSensorId: 'red',
        startingPoint: false,
        pulse: false,
      },
      '25': {
        x: 15 / 4 * 120 - 37.5,
        y: 1 / 2 * 60 * Math.sqrt(3) + 23,
        color: {
          r: 0,
          g: 123,
          b: 255,
          a: 1,
        },
        initColor: {
          r: 0,
          g: 123,
          b: 255,
          a: 1,
        },
        glowing: 'glowing',
        activationSensorId: 'blue',
        startingPoint: false,
        pulse: false,
      },
      '26': {
        x: 17 / 4 * 120 - 37.5,
        y: 1 / 2 * 60 * Math.sqrt(3) + 23,
        color: {
          r: 40,
          g: 167,
          b: 69,
          a: 1,
        },
        initColor: {
          r: 40,
          g: 167,
          b: 69,
          a: 1,
        },
        glowing: 'glowing',
        activationSensorId: 'green',
        startingPoint: false,
        pulse: false,
      },
      '31': {
        x: 8 / 4 * 120 - 37.5,
        y: 2 / 2 * 60 * Math.sqrt(3) + 23,
        color: {
          r: 0,
          g: 209,
          b: 182,
          a: 0.7,
        },
        initColor: {
          r: 0,
          g: 209,
          b: 182,
          a: 0.7,
        },
        glowing: 'glowing',
        activationSensorId: null,
        startingPoint: true,
        pulse: false,
      },
      '32': {
        x: 10 / 4 * 120 - 37.5,
        y: 2 / 2 * 60 * Math.sqrt(3) + 23,
        color: {
          r: 255,
          g: 255,
          b: 255,
          a: 1,
        },
        initColor: {
          r: 255,
          g: 255,
          b: 255,
          a: 1,
        },
        glowing: 'glowing',
        activationSensorId: 'white',
        startingPoint: false,
        pulse: false,
      },
      '33': {
        x: 12 / 4 * 120 - 37.5,
        y: 2 / 2 * 60 * Math.sqrt(3) + 23,
        color: {
          r: 253,
          g: 126,
          b: 20,
          a: 1,
        },
        initColor: {
          r: 253,
          g: 126,
          b: 20,
          a: 1,
        },
        glowing: 'glowing',
        activationSensorId: 'orange',
        startingPoint: false,
        pulse: false,
      },
      '34': {
        x: 14 / 4 * 120 - 37.5,
        y: 2 / 2 * 60 * Math.sqrt(3) + 23,
        color: {
          r: 232,
          g: 62,
          b: 140,
          a: 1,
        },
        initColor: {
          r: 232,
          g: 62,
          b: 140,
          a: 1,
        },
        glowing: 'glowing',
        activationSensorId: 'pink',
        startingPoint: false,
        pulse: false,
      },
      '35': {
        x: 16 / 4 * 120 - 37.5,
        y: 2 / 2 * 60 * Math.sqrt(3) + 23,
        color: {
          r: 255,
          g: 255,
          b: 255,
          a: 1,
        },
        initColor: {
          r: 255,
          g: 255,
          b: 255,
          a: 1,
        },
        glowing: 'glowing',
        activationSensorId: 'white',
        startingPoint: false,
        pulse: false,
      },
      '41': {
        x: 7 / 4 * 120 - 37.5,
        y: 3 / 2 * 60 * Math.sqrt(3) + 23,
        color: {
          r: 0,
          g: 209,
          b: 182,
          a: 0.7,
        },
        initColor: {
          r: 0,
          g: 209,
          b: 182,
          a: 0.7,
        },
        glowing: 'glowing',
        activationSensorId: null,
        startingPoint: true,
        pulse: false,
      },
      '42': {
        x: 9 / 4 * 120 - 37.5,
        y: 3 / 2 * 60 * Math.sqrt(3) + 23,
        color: {
          r: 0,
          g: 123,
          b: 255,
          a: 1,
        },
        initColor: {
          r: 0,
          g: 123,
          b: 255,
          a: 1,
        },
        glowing: 'glowing',
        activationSensorId: 'blue',
        startingPoint: false,
        pulse: false,
      },
      '43': {
        x: 11 / 4 * 120 - 37.5,
        y: 3 / 2 * 60 * Math.sqrt(3) + 23,
        color: {
          r: 40,
          g: 167,
          b: 69,
          a: 1,
        },
        initColor: {
          r: 40,
          g: 167,
          b: 69,
          a: 1,
        },
        glowing: 'glowing',
        activationSensorId: 'green',
        startingPoint: false,
        pulse: false,
      },
      '44': {
        x: 13 / 4 * 120 - 37.5,
        y: 3 / 2 * 60 * Math.sqrt(3) + 23,
        color: {
          r: 220,
          g: 53,
          b: 69,
          a: 1,
        },
        initColor: {
          r: 220,
          g: 53,
          b: 69,
          a: 1,
        },
        glowing: 'glowing',
        activationSensorId: 'red',
        startingPoint: false,
        pulse: false,
      },
      '45': {
        x: 15 / 4 * 120 - 37.5,
        y: 3 / 2 * 60 * Math.sqrt(3) + 23,
        color: {
          r: 0,
          g: 123,
          b: 255,
          a: 1,
        },
        initColor: {
          r: 0,
          g: 123,
          b: 255,
          a: 1,
        },
        glowing: 'glowing',
        activationSensorId: 'blue',
        startingPoint: false,
        pulse: false,
      },
      '46': {
        x: 17 / 4 * 120 - 37.5,
        y: 3 / 2 * 60 * Math.sqrt(3) + 23,
        color: {
          r: 253,
          g: 126,
          b: 20,
          a: 1,
        },
        initColor: {
          r: 253,
          g: 126,
          b: 20,
          a: 1,
        },
        glowing: 'glowing',
        activationSensorId: 'orange',
        startingPoint: false,
        pulse: false,
      },
      '51': {
        x: 8 / 4 * 120 - 37.5,
        y: 4 / 2 * 60 * Math.sqrt(3) + 23,
        color: {
          r: 0,
          g: 209,
          b: 182,
          a: 0.7,
        },
        initColor: {
          r: 0,
          g: 209,
          b: 182,
          a: 0.7,
        },
        glowing: 'glowing',
        activationSensorId: null,
        startingPoint: true,
        pulse: false,
      },
      '52': {
        x: 10 / 4 * 120 - 37.5,
        y: 4 / 2 * 60 * Math.sqrt(3) + 23,
        color: {
          r: 253,
          g: 126,
          b: 20,
          a: 1,
        },
        initColor: {
          r: 253,
          g: 126,
          b: 20,
          a: 1,
        },
        glowing: 'glowing',
        activationSensorId: 'orange',
        startingPoint: false,
        pulse: false,
      },
      '53': {
        x: 12 / 4 * 120 - 37.5,
        y: 4 / 2 * 60 * Math.sqrt(3) + 23,
        color: {
          r: 255,
          g: 255,
          b: 255,
          a: 1,
        },
        initColor: {
          r: 255,
          g: 255,
          b: 255,
          a: 1,
        },
        glowing: 'glowing',
        activationSensorId: 'white',
        startingPoint: false,
        pulse: false,
      },
      '54': {
        x: 14 / 4 * 120 - 37.5,
        y: 4 / 2 * 60 * Math.sqrt(3) + 23,
        color: {
          r: 40,
          g: 167,
          b: 69,
          a: 1,
        },
        initColor: {
          r: 40,
          g: 167,
          b: 69,
          a: 1,
        },
        glowing: 'glowing',
        activationSensorId: 'green',
        startingPoint: false,
        pulse: false,
      },
      '55': {
        x: 16 / 4 * 120 - 37.5,
        y: 4 / 2 * 60 * Math.sqrt(3) + 23,
        color: {
          r: 255,
          g: 255,
          b: 255,
          a: 1,
        },
        initColor: {
          r: 255,
          g: 255,
          b: 255,
          a: 1,
        },
        glowing: 'glowing',
        activationSensorId: 'white',
        startingPoint: false,
        pulse: false,
      },
    },
    edges: {
      '31-32': {
        getVertice1: function() {
          if (store.state.currentActivationSequence == ACTIVATION_SEQUENCE_EASY) {
            return '31'
          } else {
            return '32'
          }
        },
        getVertice2: function() {
          if (store.state.currentActivationSequence == ACTIVATION_SEQUENCE_EASY) {
            return '32'
          } else {
            return '31'
          }
        },
        color: 'rgba(255, 255, 255, 0)',
        activationPathAnimation: false,
        activated: false,
        validated: false,
        finalAnimation: false,
        getDirection: function() {
          if (store.state.currentActivationSequence == ACTIVATION_SEQUENCE_EASY) {
            return 'left-right'
          } else {
            return 'right-left'
          }
        },
      },
      '32-33': {
        getVertice1: function() {
          if (store.state.currentActivationSequence == ACTIVATION_SEQUENCE_NORMAL_AND_HARD_1 || store.state.currentActivationSequence == ACTIVATION_SEQUENCE_EASY) {
            return '32'
          } else {
            return '33'
          }
        },
        getVertice2: function() {
          if (store.state.currentActivationSequence == ACTIVATION_SEQUENCE_NORMAL_AND_HARD_1 || store.state.currentActivationSequence == ACTIVATION_SEQUENCE_EASY) {
            return '33'
          } else {
            return '32'
          }
        },
        color: 'rgba(255, 255, 255, 0)',
        activationPathAnimation: false,
        activated: false,
        validated: false,
        finalAnimation: false,
        getDirection: function() {
          if (store.state.currentActivationSequence == ACTIVATION_SEQUENCE_NORMAL_AND_HARD_1 || store.state.currentActivationSequence == ACTIVATION_SEQUENCE_EASY) {
            return 'left-right'
          } else {
            return 'right-left'
          }
        },
      },
      '33-24': {
        getVertice1: function() {
          return '33'
        },
        getVertice2: function() {
          return '24'
        },
        color: 'rgba(255, 255, 255, 0)',
        activationPathAnimation: false,
        activated: false,
        validated: false,
        finalAnimation: false,
        getDirection: function() {
          return 'bottomleft-topright'
        },
      },
      '24-25': {
        getVertice1: function() {
          return '24'
        },
        getVertice2: function() {
          return '25'
        },
        color: 'rgba(255, 255, 255, 0)',
        activationPathAnimation: false,
        activated: false,
        validated: false,
        finalAnimation: false,
        getDirection: function() {
          return 'left-right'
        },
      },
      '25-26': {
        getVertice1: function() {
          return '25'
        },
        getVertice2: function() {
          return '26'
        },
        color: 'rgba(255, 255, 255, 0)',
        activationPathAnimation: false,
        activated: false,
        validated: false,
        finalAnimation: false,
        getDirection: function() {
          return 'left-right'
        },
      },
      '51-52': {
        getVertice1: function() {
          if (store.state.currentActivationSequence == ACTIVATION_SEQUENCE_NORMAL_AND_HARD_1) {
            return '51'
          } else {
            return '52'
          }
        },
        getVertice2: function() {
          if (store.state.currentActivationSequence == ACTIVATION_SEQUENCE_NORMAL_AND_HARD_1) {
            return '52'
          } else {
            return '51'
          }
        },
        color: 'rgba(255, 255, 255, 0)',
        activationPathAnimation: false,
        activated: false,
        validated: false,
        finalAnimation: false,
        getDirection: function() {
          if (store.state.currentActivationSequence == ACTIVATION_SEQUENCE_NORMAL_AND_HARD_1) {
            return 'left-right'
          } else {
            return 'right-left'
          }
        },
      },
      '52-43': {
        getVertice1: function() {
          if (store.state.currentActivationSequence == ACTIVATION_SEQUENCE_NORMAL_AND_HARD_1) {
            return '52'
          } else {
            return '43'
          }
        },
        getVertice2: function() {
          if (store.state.currentActivationSequence == ACTIVATION_SEQUENCE_NORMAL_AND_HARD_1) {
            return '43'
          } else {
            return '52'
          }
        },
        color: 'rgba(255, 255, 255, 0)',
        activationPathAnimation: false,
        activated: false,
        validated: false,
        finalAnimation: false,
        getDirection: function() {
          if (store.state.currentActivationSequence == ACTIVATION_SEQUENCE_NORMAL_AND_HARD_1) {
            return 'bottomleft-topright'
          } else {
            return 'topright-bottomleft'
          }
        },
      },
      '43-32': {
        getVertice1: function() {
          if (store.state.currentActivationSequence == ACTIVATION_SEQUENCE_NORMAL_AND_HARD_1) {
            return '43'
          } else {
            return '32'
          }
        },
        getVertice2: function() {
          if (store.state.currentActivationSequence == ACTIVATION_SEQUENCE_NORMAL_AND_HARD_1) {
            return '32'
          } else {
            return '43'
          }
        },
        color: 'rgba(255, 255, 255, 0)',
        activationPathAnimation: false,
        activated: false,
        validated: false,
        finalAnimation: false,
        getDirection: function() {
          if (store.state.currentActivationSequence == ACTIVATION_SEQUENCE_NORMAL_AND_HARD_1) {
            return 'bottomright-topleft'
          } else {
            return 'topleft-bottomright'
          }
        },
      },
      '32-23': {
        getVertice1: function() {
          if (store.state.currentActivationSequence == ACTIVATION_SEQUENCE_NORMAL_AND_HARD_1) {
            return '32'
          } else {
            return '23'
          }
        },
        getVertice2: function() {
          if (store.state.currentActivationSequence == ACTIVATION_SEQUENCE_NORMAL_AND_HARD_1) {
            return '23'
          } else {
            return '32'
          }
        },
        color: 'rgba(255, 255, 255, 0)',
        activationPathAnimation: false,
        activated: false,
        validated: false,
        finalAnimation: false,
        getDirection: function() {
          if (store.state.currentActivationSequence == ACTIVATION_SEQUENCE_NORMAL_AND_HARD_1) {
            return 'bottomleft-topright'
          } else {
            return 'topright-bottomleft'
          }
        },
      },
      '23-24': {
        getVertice1: function() {
          return '23'
        },
        getVertice2: function() {
          return '24'
        },
        color: 'rgba(255, 255, 255, 0)',
        activationPathAnimation: false,
        activated: false,
        validated: false,
        finalAnimation: false,
        getDirection: function() {
          return 'left-right'
        },
      },
      '24-34': {
        getVertice1: function() {
          if (store.state.currentActivationSequence == ACTIVATION_SEQUENCE_NORMAL_AND_HARD_1 || store.state.currentActivationSequence == ACTIVATION_SEQUENCE_EASY) {
            return '24'
          } else {
            return '34'
          }
        },
        getVertice2: function() {
          if (store.state.currentActivationSequence == ACTIVATION_SEQUENCE_NORMAL_AND_HARD_1 || store.state.currentActivationSequence == ACTIVATION_SEQUENCE_EASY) {
            return '34'
          } else {
            return '24'
          }
        },
        color: 'rgba(255, 255, 255, 0)',
        activationPathAnimation: false,
        activated: false,
        validated: false,
        finalAnimation: false,
        getDirection: function() {
          if (store.state.currentActivationSequence == ACTIVATION_SEQUENCE_NORMAL_AND_HARD_1 || store.state.currentActivationSequence == ACTIVATION_SEQUENCE_EASY) {
            return 'topleft-bottomright'
          } else {
            return 'bottomright-topleft'
          }
        },
      },
      '34-35': {
        getVertice1: function() {
          return '34'
        },
        getVertice2: function() {
          return '35'
        },
        color: 'rgba(255, 255, 255, 0)',
        activationPathAnimation: false,
        activated: false,
        validated: false,
        finalAnimation: false,
        getDirection: function() {
          return 'left-right'
        },
      },
      '11-12': {
        getVertice1: function() {
          if (store.state.currentActivationSequence == ACTIVATION_SEQUENCE_HARD_2) {
            return '11'
          } else {
            return '12'
          }
        },
        getVertice2: function() {
          if (store.state.currentActivationSequence == ACTIVATION_SEQUENCE_HARD_2) {
            return '12'
          } else {
            return '11'
          }
        },
        color: 'rgba(255, 255, 255, 0)',
        activationPathAnimation: false,
        activated: false,
        validated: false,
        finalAnimation: false,
        getDirection: function() {
          if (store.state.currentActivationSequence == ACTIVATION_SEQUENCE_HARD_2) {
            return 'left-right'
          } else {
            return 'right-left'
          }
        },
      },
      '12-23': {
        getVertice1: function() {
          if (store.state.currentActivationSequence == ACTIVATION_SEQUENCE_HARD_2) {
            return '12'
          } else {
            return '23'
          }
        },
        getVertice2: function() {
          if (store.state.currentActivationSequence == ACTIVATION_SEQUENCE_HARD_2) {
            return '23'
          } else {
            return '12'
          }
        },
        color: 'rgba(255, 255, 255, 0)',
        activationPathAnimation: false,
        activated: false,
        validated: false,
        finalAnimation: false,
        getDirection: function() {
          if (store.state.currentActivationSequence == ACTIVATION_SEQUENCE_HARD_2) {
            return 'topleft-bottomright'
          } else {
            return 'bottomright-topleft'
          }
        },
      },
      '43-44': {
        getVertice1: function() {
          if (store.state.currentActivationSequence == ACTIVATION_SEQUENCE_HARD_2) {
            return '43'
          } else {
            return '44'
          }
        },
        getVertice2: function() {
          if (store.state.currentActivationSequence == ACTIVATION_SEQUENCE_HARD_2) {
            return '44'
          } else {
            return '43'
          }
        },
        color: 'rgba(255, 255, 255, 0)',
        activationPathAnimation: false,
        activated: false,
        validated: false,
        finalAnimation: false,
        getDirection: function() {
          if (store.state.currentActivationSequence == ACTIVATION_SEQUENCE_HARD_2) {
            return 'left-right'
          } else {
            return 'right-left'
          }
        },
      },
      '44-34': {
        getVertice1: function() {
          if (store.state.currentActivationSequence == ACTIVATION_SEQUENCE_HARD_2) {
            return '44'
          } else {
            return '34'
          }
        },
        getVertice2: function() {
          if (store.state.currentActivationSequence == ACTIVATION_SEQUENCE_HARD_2) {
            return '34'
          } else {
            return '44'
          }
        },
        color: 'rgba(255, 255, 255, 0)',
        activationPathAnimation: false,
        activated: false,
        validated: false,
        finalAnimation: false,
        getDirection: function() {
          if (store.state.currentActivationSequence == ACTIVATION_SEQUENCE_HARD_2) {
            return 'bottomleft-topright'
          } else {
            return 'topright-bottomleft'
          }
        },
      }
    },
    activationSequences: {
      easy: [
        ACTIVATION_SEQUENCE_EASY,
      ],
      normal: [
        ACTIVATION_SEQUENCE_NORMAL_AND_HARD_1,
      ],
      hard: [
        ACTIVATION_SEQUENCE_NORMAL_AND_HARD_1,
        ACTIVATION_SEQUENCE_HARD_2,
      ],
    },
    activatedSensors: [],
    currentActivationSequence: [],
    colorDefault: 'rgba(255, 255, 255, 0)',
    colorActivation: 'rgba(255, 255, 255, 0.4)',
    colorValidated: 'rgba(255, 255, 255, 1)',
    activationAnimation: null,
    playable: true,
    transparentVertices: false,
    showGlobalError: false,
    colorTriangles: {
      blue: false,
      orange: false,
      white: false,
      green: false,
      red: false,
      pink: false,
    },
    nextActivationHelpTask: null,
    isRestaurantInManualMode: false,
    gameOverCounter: -1,
    pinkGameOverCounter: -2,
    lightOverloadCounter: -1,
  },
  getters: {
    currentActivationEdgeId (state) {
      for (var i = 0 ; i < state.currentActivationSequence.length ; i++) {
        var edgeId = state.currentActivationSequence[i]
        var edge = state.edges[edgeId]

        if (!edge.validated) {
          return edgeId
        }
      }

      return null
    },
    nextActivationEdgeId (state) {
      var thisIsTheNextOne = false

      for (var i = 0 ; i < state.currentActivationSequence.length ; i++) {
        var edgeId = state.currentActivationSequence[i]
        if (thisIsTheNextOne) {
          return edgeId
        }

        var edge = state.edges[edgeId]
        if (!edge.validated) {
          thisIsTheNextOne = true
        }
      }

      return null
    },
    currentDeactivationEdgeId (state) {
      for (var i = state.currentActivationSequence.length - 1 ; i >= 0 ; i--) {
        var edgeId = state.currentActivationSequence[i]
        var edge = state.edges[edgeId]

        if (edge.activated) {
          return edgeId
        }
      }

      return null
    },
    nextFinalAnimationEdgeIds (state) {
      var validatedEdgeIds = Object.keys(state.edges).filter(
        function (key) {return state.edges[key].validated === true})

      var validatedEdgeVertices = []
      for (var i = 0 ; i < validatedEdgeIds.length ; i++) {
        validatedEdgeVertices.push(state.edges[validatedEdgeIds[i]].getVertice1())
        validatedEdgeVertices.push(state.edges[validatedEdgeIds[i]].getVertice2())
      }

      var edgesToAnimate = Object.keys(state.edges).filter(
        function (key) {
          return (
            state.edges[key].validated === false &&
            (validatedEdgeVertices.includes(state.edges[key].getVertice1()) || validatedEdgeVertices.includes(state.edges[key].getVertice2()))
          )
        }
      )

      return edgesToAnimate
    },
  },
  mutations: {
    gameOverCounterPlusPlus (state) {
      state.gameOverCounter++
    },
    pinkGameOverCounterPlusPlus (state) {
      state.pinkGameOverCounter++
    },
    showColorTriangles (state, color) {
      state.colorTriangles[color] = true
    },
    hideColorTriangles (state, color) {
      state.colorTriangles[color] = false
    },
    anticipateNextActivation (state, nextVertice) {
      state.nextActivationHelpTask = setTimeout(store.commit, 2500, 'showColorTriangles', nextVertice.activationSensorId)
    },
    cancelNextActivationAnticipation (state) {
      clearTimeout(state.nextActivationHelpTask)
    },
    setVerticesTransparent (state) {
      state.transparentVertices = true
    },
    setPlayable (state) {
      state.playable = true
    },
    setUnplayable (state) {
      state.playable = false

      for (let [, vertice] of Object.entries(state.vertices)) {
        vertice.pulse = false
      }

      if (store.state.activationAnimation !== null) {
        store.state.activationAnimation.pause()
        store.state.activationAnimation = null
      }
    },
    setEdgeActivationPathAnimation (state, edgeId) {
      state.edges[edgeId].activationPathAnimation = true
    },
    unsetEdgeActivationPathAnimation (state, edgeId) {
      state.edges[edgeId].activationPathAnimation = false
    },
    activateEdge (state, edgeId) {
      state.edges[edgeId].activated = true
    },
    validateEdge (state, edgeId) {
      state.edges[edgeId].validated = true
    },
    deactivateEdge (state, edgeId) {
      state.edges[edgeId].activated = false
    },
    invalidateEdge (state, edgeId) {
      state.edges[edgeId].validated = false
    },
    setEdgeFinalAnimation (state, edgeId) {
      state.edges[edgeId].finalAnimation = true
    },
    setActivationAnimation (state, activationAnimation) {
      state.activationAnimation = activationAnimation
    },
    setVerticePulseScale (state, {verticeId, pulseIndex, scale}) {
      state.vertices[verticeId].pulses[pulseIndex].scale = scale
    },
    setVerticePulseOpacity (state, {verticeId, pulseIndex, opacity}) {
      state.vertices[verticeId].pulses[pulseIndex].opacity = opacity
    },
    startVerticePulse (state, verticeId) {
      state.vertices[verticeId].pulse = true
    },
    stopVerticePulse (state, verticeId) {
      state.vertices[verticeId].pulse = false
    },
    setVerticeGlow (state, {verticeId, glow}) {
      state.vertices[verticeId].glowing = glow
    },
    setVerticeRGBA (state, {verticeId, r, g, b, a}) {
      state.vertices[verticeId].color.r = r
      state.vertices[verticeId].color.g = g
      state.vertices[verticeId].color.b = b
      state.vertices[verticeId].color.a = a
    },
    loadNextActivationSequence (state) {
      let currentSequenceIndex = state.activationSequences[difficultyStore.state.difficulty].indexOf(state.currentActivationSequence)
      let nextSequenceIndex = (currentSequenceIndex + 1) % state.activationSequences[difficultyStore.state.difficulty].length
      state.currentActivationSequence = state.activationSequences[difficultyStore.state.difficulty][nextSequenceIndex]
    },
    loadFirstActivationSequence (state) {
      state.currentActivationSequence = state.activationSequences[difficultyStore.state.difficulty][0]
    },
    setEdgeColor (state, {edgeId, color}) {
      state.edges[edgeId].color = color
    },
    resetActivationSequenceEdgesColor (state) {
      var white = store.state.colorDefault
      for (var i = 0 ; i < state.currentActivationSequence.length ; i++) {
        var edgeId = state.currentActivationSequence[i]
        state.edges[edgeId].color = white
      }
    },
    setRestaurantInManualMode(state) {
      state.isRestaurantInManualMode = true
    },
    toggleColor (state, {currentVertice, color, activated}) {
      if (!state.isRestaurantInManualMode || progressionStore.state.lightServiceSuccess) {
        return
      }

      if (activated === true) {
        if (!state.activatedSensors.includes(color)) {
          state.activatedSensors.push(color)
        }
      } else {
        state.activatedSensors = state.activatedSensors.filter(
          function(ele) {
            return ele != color
          }
        )
      }

      if (state.playable) {
        if (activated === true) {
          if (state.activationAnimation === null) {
            if (currentVertice.activationSensorId == color) {
              nextActivation()
            }
          }

          if (state.activatedSensors.length > 4) {
            state.lightOverloadCounter++
            if (state.lightOverloadCounter % 3 === 0) {
              lightLogStore.commit("processLog", {logMessage: "too_many_lights_on", level: "info", useLocale: true})
            }
          }
        } else {
          if (state.activationAnimation) {
            if (currentVertice.activationSensorId == color) {
              if (state.edges[state.currentActivationSequence[0]].validated) {
                gameOver(newActivationSequence, true)
                store.dispatch("recordGameOver", "current_light_off")
              } else {
                gameOver(setPlayable, false, null)
              }
            }
          }
        }
      }
    },
    showGlobalError (state) {
      state.showGlobalError = true
    },
    hideGlobalError (state) {
      state.showGlobalError = false
    },
  },
  actions: {
    init (context) {
      context.commit('loadFirstActivationSequence')

      var color = store.state.colorActivation
      for (var i = 0 ; i < context.state.currentActivationSequence.length ; i++) {
        var edgeId = context.state.currentActivationSequence[i]
        context.commit('setEdgeColor', {edgeId, color})
      }

      context.commit('setRestaurantInManualMode')
    },
    toggleColor (context, {color, activated}) {
      if (!context.state.isRestaurantInManualMode) {
        return
      }

      var currentVertice = context.state.vertices[context.state.edges[context.getters.currentActivationEdgeId].getVertice2()]

      context.commit('toggleColor', {currentVertice, color, activated})

      if (color === 'red' || color === 'white') {
        var complementaryColor = 'red'
        if (color === 'red') {
          complementaryColor = 'white'
        }

        let isComplementaryColorActivated = context.state.activatedSensors.slice(0, 4).includes(complementaryColor)
        let pinkActivation = activated && isComplementaryColorActivated

        // Only notify in case of diff
        if (context.state.activatedSensors.includes('pink') !== pinkActivation) {
          context.commit(
            'toggleColor',
            {
              currentVertice: currentVertice,
              color: 'pink',
              activated: pinkActivation,
            }
          )
        }
      }
    },
    recordGameOver (context, reason) {
      publishSubscribeService.commit(
        'publish',
        {
          "category": "light_game_over",
          "reason": reason,
          "edgeId": context.getters.currentActivationEdgeId,
          "sequence": context.state.currentActivationSequence,
        }
      )
      if (reason === "pink_not_on") {
        context.commit('pinkGameOverCounterPlusPlus')
        if (store.state.pinkGameOverCounter % 2 === 0) {
          lightLogStore.commit("processLog", {logMessage: "pink_was_not_pressed", level: "info", useLocale: true})
        }
      } else {
        context.commit('gameOverCounterPlusPlus')
        if (store.state.gameOverCounter % 3 === 0) {
          if (reason === "next_light_not_on") {
            lightLogStore.commit("processLog", {logMessage: "the_next_light_was_not_pressed", level: "warning", useLocale: true})
          } else if (reason === "current_light_off") {
            lightLogStore.commit("processLog", {logMessage: "the_light_has_been_turned_off", level: "warning", useLocale: true})
          }
        }
      }
    },
  }
})

export default store
