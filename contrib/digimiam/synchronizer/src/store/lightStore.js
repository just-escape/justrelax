import Vue from 'vue'
import Vuex from 'vuex'

import difficultyStore from '@/store/difficultyStore.js'

Vue.use(Vuex)


const ACTIVATION_SEQUENCE_EASY_1 = [
  '21-22',
  '22-23',
  '23-24',
  '24-25',
  '25-26',
  '26-27',
]

const ACTIVATION_SEQUENCE_NORMAL_1 = [
  '41-42',
  '42-52',
  '52-43',
  '43-32',
  '32-33',
  '33-24',
  '24-34',
  '34-35',
  '35-46',
  '46-36',
]

const ACTIVATION_SEQUENCE_HARD_1 = [
  '61-62',
  '62-72',
  '72-73',
  '73-74',
  '74-65',
  '65-64',
  '64-54',
  '54-55',
  '55-45',
  '45-44',
  '44-53',
  '53-63',
  '63-52',
  '52-43',
  '43-32',
  '32-33',
  '33-24',
  '24-34',
  '34-35',
  '35-46',
  '46-36',
]

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
    offset: '100%',
  })
  .add({
    duration: 2000,
    targets: '.gradientColor2',
    offset: '110%',
  }, '-=2000')
  .add({
    duration: 2000,
    update(anim) {
      var rotation = anim.progress * 360 / 100
      for (var i = 0 ; i < edgeIds.length ; i++) {
        var verticeId = store.state.edges[edgeIds[i]].getVertice2()
        store.commit('setVerticeRotation', {verticeId, rotation})
      }
    },
  }, '-=2000')
  .add({
    duration: 1500,
    targets: '#glowing-transition-intensity',
    stdDeviation: "20",
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
    stdDeviation: "2",
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
    },
    complete: function() {
      store.commit('validateEdge', edgeId)
      var glow = 'glowing-more'
      store.commit('setVerticeGlow', {verticeId, glow})
      nextActivation()
    },
  })
  .add({
    duration: 3000,
    targets: '.gradientColor1',
    offset: '100%',
  })
  .add({
    duration: 3000,
    targets: '.gradientColor2',
    offset: '110%',
  }, '-=3000')
  .add({
    duration: 3000,
    update(anim) {
      var rotation = anim.progress * 360 / 100
      store.commit('setVerticeRotation', {verticeId, rotation})
    },
  }, '-=3000')
  .add({
    duration: 2500,
    targets: '#glowing-transition-intensity',
    stdDeviation: "20",
  }, '-=2500')
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
    stdDeviation: "2",
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
    if (store.state.sensors[store.state.vertices[store.state.edges[edgeId].getVertice2()].activationSensorId] === true) {
      activateEdge(edgeId)
    } else {
      nextActivationSequence()
    }
  }
}

function confirmationAnimation() {
  var i = 0
  var verticeIds = []

  for (i = 0 ; i < store.state.currentActivationSequence.length ; i++) {
    var v1 = store.state.edges[store.state.currentActivationSequence[i]].getVertice1()
    if (!verticeIds.includes(v1)) {
      verticeIds.push(v1)
    }

    var v2 = store.state.edges[store.state.currentActivationSequence[i]].getVertice2()
    if (!verticeIds.includes(v2)) {
      verticeIds.push(v2)
    }
  }

  var rotationAnimation = {
    duration: 1200,
    easing: 'linear',
    update(anim) {
      var rotation = anim.progress * 180 / 100
      for (i = 0 ; i < verticeIds.length ; i++) {
        var verticeId = verticeIds[i]
        store.commit('setVerticeRotation', {verticeId, rotation})
      }
    },
  }

  Vue.prototype.$anime.timeline({
    complete: function() {
      setTimeout(propagateFinalAnimation, 750)
    }
  })
  .add(rotationAnimation, '+=250')
  .add(rotationAnimation, '+=500')
}

function _deactivateEdge(edgeId) {
  var verticeId = store.state.edges[edgeId].getVertice2()

  var rotationReference = store.state.vertices[verticeId].rotation

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
      nextDeactivation()
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
    update(anim) {
      var rotation = rotationReference - (rotationReference * anim.progress / 100)
      store.commit('setVerticeRotation', {verticeId, rotation})
    },
  }, '-=1000')
  .add({
    duration: 1000,
    targets: '#glowing-transition-intensity',
    stdDeviation: "2",
  }, '-=1000')
}

function deactivateEdge(edgeId) {
  /* If the deactivation sequence happens after an edge has been validated
   * and because conditions are not met to activate the next one, some
   * values have already been reset, so we need to preset them. Otherwise,
   * in the middle of the activation animation, values are already good ones.
   */
  if (store.state.edges[edgeId].validated) {
    Vue.prototype.$anime.timeline({
      complete: function() {
        _deactivateEdge(edgeId)
      }
    })
    .add({
      duration: 1,
      targets: '.gradientColor1',
      offset: '100%',
    })
    .add({
      duration: 1,
      targets: '.gradientColor2',
      offset: '110%',
    }, '-=1')
    .add({
      duration: 1,
      targets: '#glowing-transition-intensity',
      stdDeviation: "20",
    }, '-=1')
  } else {
    _deactivateEdge(edgeId)
  }
}

function nextDeactivation() {
  var edgeId = store.getters.currentDeactivationEdgeId

  if (edgeId === null) {
    store.commit('resetActivationSequenceEdgesColor')

    store.commit('loadNextActivationSequence')
    newActivationSequence()
  } else {
    deactivateEdge(edgeId)
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
    offset: '100%',
  })
  .add({
    duration: 350,
    targets: '.gradientColor2',
    offset: '110%',
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
  newActivationPath()
}

function nextActivationSequence() {
  store.commit('setUnplayable')

  nextDeactivation()
}

var store = new Vuex.Store({
  state: {
    vertices: {
      '11': {
        x: 8 / 4 * 120 - 37.5,
        y: 0 / 2 * 60 * Math.sqrt(3) + 23,
        rotation: 0,
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
      },
      '12': {
        x: 10 / 4 * 120 - 37.5,
        y: 0 / 2 * 60 * Math.sqrt(3) + 23,
        rotation: 0,
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
      },
      '13': {
        x: 12 / 4 * 120 - 37.5,
        y: 0 / 2 * 60 * Math.sqrt(3) + 23,
        rotation: 0,
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
      },
      '14': {
        x: 14 / 4 * 120 - 37.5,
        y: 0 / 2 * 60 * Math.sqrt(3) + 23,
        rotation: 0,
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
      },
      '15': {
        x: 16 / 4 * 120 - 37.5,
        y: 0 / 2 * 60 * Math.sqrt(3) + 23,
        rotation: 0,
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
      },
      '16': {
        x: 18 / 4 * 120 - 37.5,
        y: 0 / 2 * 60 * Math.sqrt(3) + 23,
        rotation: 0,
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
      },
      '21': {
        x: 7 / 4 * 120 - 37.5,
        y: 1 / 2 * 60 * Math.sqrt(3) + 23,
        rotation: 0,
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
      },
      '22': {
        x: 9 / 4 * 120 - 37.5,
        y: 1 / 2 * 60 * Math.sqrt(3) + 23,
        rotation: 0,
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
      },
      '23': {
        x: 11 / 4 * 120 - 37.5,
        y: 1 / 2 * 60 * Math.sqrt(3) + 23,
        rotation: 0,
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
      },
      '24': {
        x: 13 / 4 * 120 - 37.5,
        y: 1 / 2 * 60 * Math.sqrt(3) + 23,
        rotation: 0,
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
      },
      '25': {
        x: 15 / 4 * 120 - 37.5,
        y: 1 / 2 * 60 * Math.sqrt(3) + 23,
        rotation: 0,
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
      },
      '26': {
        x: 17 / 4 * 120 - 37.5,
        y: 1 / 2 * 60 * Math.sqrt(3) + 23,
        rotation: 0,
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
      },
      '27': {
        x: 19 / 4 * 120 - 37.5,
        y: 1 / 2 * 60 * Math.sqrt(3) + 23,
        rotation: 0,
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
      },
      '31': {
        x: 8 / 4 * 120 - 37.5,
        y: 2 / 2 * 60 * Math.sqrt(3) + 23,
        rotation: 0,
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
      },
      '32': {
        x: 10 / 4 * 120 - 37.5,
        y: 2 / 2 * 60 * Math.sqrt(3) + 23,
        rotation: 0,
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
      },
      '33': {
        x: 12 / 4 * 120 - 37.5,
        y: 2 / 2 * 60 * Math.sqrt(3) + 23,
        rotation: 0,
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
      },
      '34': {
        x: 14 / 4 * 120 - 37.5,
        y: 2 / 2 * 60 * Math.sqrt(3) + 23,
        rotation: 0,
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
      },
      '35': {
        x: 16 / 4 * 120 - 37.5,
        y: 2 / 2 * 60 * Math.sqrt(3) + 23,
        rotation: 0,
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
      },
      '36': {
        x: 18 / 4 * 120 - 37.5,
        y: 2 / 2 * 60 * Math.sqrt(3) + 23,
        rotation: 0,
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
      },
      '41': {
        x: 7 / 4 * 120 - 37.5,
        y: 3 / 2 * 60 * Math.sqrt(3) + 23,
        rotation: 0,
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
      },
      '42': {
        x: 9 / 4 * 120 - 37.5,
        y: 3 / 2 * 60 * Math.sqrt(3) + 23,
        rotation: 0,
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
      },
      '43': {
        x: 11 / 4 * 120 - 37.5,
        y: 3 / 2 * 60 * Math.sqrt(3) + 23,
        rotation: 0,
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
      },
      '44': {
        x: 13 / 4 * 120 - 37.5,
        y: 3 / 2 * 60 * Math.sqrt(3) + 23,
        rotation: 0,
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
      },
      '45': {
        x: 15 / 4 * 120 - 37.5,
        y: 3 / 2 * 60 * Math.sqrt(3) + 23,
        rotation: 0,
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
      },
      '46': {
        x: 17 / 4 * 120 - 37.5,
        y: 3 / 2 * 60 * Math.sqrt(3) + 23,
        rotation: 0,
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
      },
      '47': {
        x: 19 / 4 * 120 - 37.5,
        y: 3 / 2 * 60 * Math.sqrt(3) + 23,
        rotation: 0,
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
      },
      '51': {
        x: 8 / 4 * 120 - 37.5,
        y: 4 / 2 * 60 * Math.sqrt(3) + 23,
        rotation: 0,
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
      },
      '52': {
        x: 10 / 4 * 120 - 37.5,
        y: 4 / 2 * 60 * Math.sqrt(3) + 23,
        rotation: 0,
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
      },
      '53': {
        x: 12 / 4 * 120 - 37.5,
        y: 4 / 2 * 60 * Math.sqrt(3) + 23,
        rotation: 0,
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
      },
      '54': {
        x: 14 / 4 * 120 - 37.5,
        y: 4 / 2 * 60 * Math.sqrt(3) + 23,
        rotation: 0,
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
      },
      '55': {
        x: 16 / 4 * 120 - 37.5,
        y: 4 / 2 * 60 * Math.sqrt(3) + 23,
        rotation: 0,
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
      },
      '56': {
        x: 18 / 4 * 120 - 37.5,
        y: 4 / 2 * 60 * Math.sqrt(3) + 23,
        rotation: 0,
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
      },
      '61': {
        x: 7 / 4 * 120 - 37.5,
        y: 5 / 2 * 60 * Math.sqrt(3) + 23,
        rotation: 0,
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
      },
      '62': {
        x: 9 / 4 * 120 - 37.5,
        y: 5 / 2 * 60 * Math.sqrt(3) + 23,
        rotation: 0,
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
      },
      '63': {
        x: 11 / 4 * 120 - 37.5,
        y: 5 / 2 * 60 * Math.sqrt(3) + 23,
        rotation: 0,
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
      },
      '64': {
        x: 13 / 4 * 120 - 37.5,
        y: 5 / 2 * 60 * Math.sqrt(3) + 23,
        rotation: 0,
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
      },
      '65': {
        x: 15 / 4 * 120 - 37.5,
        y: 5 / 2 * 60 * Math.sqrt(3) + 23,
        rotation: 0,
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
      },
      '66': {
        x: 17 / 4 * 120 - 37.5,
        y: 5 / 2 * 60 * Math.sqrt(3) + 23,
        rotation: 0,
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
      },
      '67': {
        x: 19 / 4 * 120 - 37.5,
        y: 5 / 2 * 60 * Math.sqrt(3) + 23,
        rotation: 0,
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
      },
      '71': {
        x: 8 / 4 * 120 - 37.5,
        y: 6 / 2 * 60 * Math.sqrt(3) + 23,
        rotation: 0,
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
      },
      '72': {
        x: 10 / 4 * 120 - 37.5,
        y: 6 / 2 * 60 * Math.sqrt(3) + 23,
        rotation: 0,
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
      },
      '73': {
        x: 12 / 4 * 120 - 37.5,
        y: 6 / 2 * 60 * Math.sqrt(3) + 23,
        rotation: 0,
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
      },
      '74': {
        x: 14 / 4 * 120 - 37.5,
        y: 6 / 2 * 60 * Math.sqrt(3) + 23,
        rotation: 0,
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
      },
      '75': {
        x: 16 / 4 * 120 - 37.5,
        y: 6 / 2 * 60 * Math.sqrt(3) + 23,
        rotation: 0,
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
      },
      '76': {
        x: 18 / 4 * 120 - 37.5,
        y: 6 / 2 * 60 * Math.sqrt(3) + 23,
        rotation: 0,
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
      },
    },
    edges: {
      '41-42': {
        getVertice1: function () {
          return '41'
        },
        getVertice2: function() {
          return '42'
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
      '42-52': {
        getVertice1: function() {
          return '42'
        },
        getVertice2: function() {
          return '52'
        },
        color: 'rgba(255, 255, 255, 0)',
        activationPathAnimation: false,
        activated: false,
        validated: false,
        finalAnimation: false,
        getDirection: function() {
          return 'topleft-bottomright'
        },
      },
      '52-43': {
        getVertice1: function() {
          return '52'
        },
        getVertice2: function() {
          return '43'
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
      '43-32': {
        getVertice1: function() {
          return '43'
        },
        getVertice2: function() {
          return '32'
        },
        color: 'rgba(255, 255, 255, 0)',
        activationPathAnimation: false,
        activated: false,
        validated: false,
        finalAnimation: false,
        getDirection: function() {
          return 'bottomright-topleft'
        },
      },
      '32-33': {
        getVertice1: function() {
          return '32'
        },
        getVertice2: function() {
          return '33'
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
      '24-34': {
        getVertice1: function() {
          return '24'
        },
        getVertice2: function() {
          return '34'
        },
        color: 'rgba(255, 255, 255, 0)',
        activationPathAnimation: false,
        activated: false,
        validated: false,
        finalAnimation: false,
        getDirection: function() {
          return 'topleft-bottomright'
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
      '35-46': {
        getVertice1: function() {
          return '35'
        },
        getVertice2: function() {
          return '46'
        },
        color: 'rgba(255, 255, 255, 0)',
        activationPathAnimation: false,
        activated: false,
        validated: false,
        finalAnimation: false,
        getDirection: function() {
          return 'topleft-bottomright'
        },
      },
      '46-36': {
        getVertice1: function() {
          return '46'
        },
        getVertice2: function() {
          return '36'
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
      '21-22': {
        getVertice1: function() {
          return '21'
        },
        getVertice2: function() {
          return '22'
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
      '22-23': {
        getVertice1: function() {
          return '22'
        },
        getVertice2: function() {
          return '23'
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
          if (store.state.currentActivationSequence == ACTIVATION_SEQUENCE_EASY_1) {
            return 'left-right'
          } else {
            return 'left-right'
          }
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
          if (store.state.currentActivationSequence == ACTIVATION_SEQUENCE_EASY_1) {
            return 'left-right'
          } else {
            return 'left-right'
          }
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
      '26-27': {
        getVertice1: function() {
          if (store.state.currentActivationSequence == ACTIVATION_SEQUENCE_EASY_1) {
            return '26'
          } else {
            return '26'
          }
        },
        getVertice2: function() {
          if (store.state.currentActivationSequence == ACTIVATION_SEQUENCE_EASY_1) {
            return '27'
          } else {
            return '27'
          }
        },
        color: 'rgba(255, 255, 255, 0)',
        activationPathAnimation: false,
        activated: false,
        validated: false,
        finalAnimation: false,
        getDirection: function() {
          if (store.state.currentActivationSequence == ACTIVATION_SEQUENCE_EASY_1) {
            return 'left-right'
          } else {
            return 'left-right'
          }
        },
      },
      '61-62': {
        getVertice1: function() {
          return '61'
        },
        getVertice2: function() {
          return '62'
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
      '62-72': {
        getVertice1: function() {
          return '62'
        },
        getVertice2: function() {
          return '72'
        },
        color: 'rgba(255, 255, 255, 0)',
        activationPathAnimation: false,
        activated: false,
        validated: false,
        finalAnimation: false,
        getDirection: function() {
          return 'topleft-bottomright'
        },
      },
      '72-73': {
        getVertice1: function() {
          return '72'
        },
        getVertice2: function() {
          return '73'
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
      '73-74': {
        getVertice1: function() {
          return '73'
        },
        getVertice2: function() {
          return '74'
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
      '74-65': {
        getVertice1: function() {
          return '74'
        },
        getVertice2: function() {
          return '65'
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
      '65-64': {
        getVertice1: function() {
          return '65'
        },
        getVertice2: function() {
          return '64'
        },
        color: 'rgba(255, 255, 255, 0)',
        activationPathAnimation: false,
        activated: false,
        validated: false,
        finalAnimation: false,
        getDirection: function() {
          return 'right-left'
        },
      },
      '64-54': {
        getVertice1: function() {
          return '64'
        },
        getVertice2: function() {
          return '54'
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
      '54-55': {
        getVertice1: function() {
          return '54'
        },
        getVertice2: function() {
          return '55'
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
      '55-45': {
        getVertice1: function() {
          return '55'
        },
        getVertice2: function() {
          return '45'
        },
        color: 'rgba(255, 255, 255, 0)',
        activationPathAnimation: false,
        activated: false,
        validated: false,
        finalAnimation: false,
        getDirection: function() {
          return 'bottomright-topleft'
        },
      },
      '45-44': {
        getVertice1: function() {
          return '45'
        },
        getVertice2: function() {
          return '44'
        },
        color: 'rgba(255, 255, 255, 0)',
        activationPathAnimation: false,
        activated: false,
        validated: false,
        finalAnimation: false,
        getDirection: function() {
          return 'right-left'
        },
      },
      '44-53': {
        getVertice1: function() {
          return '44'
        },
        getVertice2: function() {
          return '53'
        },
        color: 'rgba(255, 255, 255, 0)',
        activationPathAnimation: false,
        activated: false,
        validated: false,
        finalAnimation: false,
        getDirection: function() {
          return 'topright-bottomleft'
        },
      },
      '53-63': {
        getVertice1: function() {
          return '53'
        },
        getVertice2: function() {
          return '63'
        },
        color: 'rgba(255, 255, 255, 0)',
        activationPathAnimation: false,
        activated: false,
        validated: false,
        finalAnimation: false,
        getDirection: function() {
          return 'topright-bottomleft'
        },
      },
      '63-52': {
        getVertice1: function() {
          return '63'
        },
        getVertice2: function() {
          return '52'
        },
        color: 'rgba(255, 255, 255, 0)',
        activationPathAnimation: false,
        activated: false,
        validated: false,
        finalAnimation: false,
        getDirection: function() {
          return 'bottomright-topleft'
        },
      },
    },
    activationSequences: {
      easy: [
        ACTIVATION_SEQUENCE_EASY_1,
      ],
      normal: [
        ACTIVATION_SEQUENCE_NORMAL_1,
      ],
      hard: [
        ACTIVATION_SEQUENCE_HARD_1,
      ],
    },
    sensors: {
      'white': false,
      'red': false,
      'blue': false,
      'orange': false,
      'green': false,
      'pink': false,
    },
    currentActivationSequence: [],
    colorDefault: 'rgba(255, 255, 255, 0)',
    colorActivation: 'rgba(255, 255, 255, 0.3)',
    colorValidated: 'rgba(0, 209, 182, 0.6)',
    activationAnimation: null,
    playable: true,
    transparentVertices: false,
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
    setVerticesTransparent (state) {
      state.transparentVertices = true
    },
    setPlayable (state) {
      state.playable = true
    },
    setUnplayable (state) {
      state.playable = false
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
    setVerticeRotation (state, {verticeId, rotation}) {
      state.vertices[verticeId].rotation = rotation
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
    toggleColor (state, {currentVertice, color, activated}) {
      if (!Object.keys(state.sensors).includes(color)) {
        // eslint-disable-next-line
        console.error("Unknown color " + color)
        return
      }

      if (activated !== true && activated !== false) {
        // eslint-disable-next-line
        console.error("Activated must be true or false (received '" + activated + "')")
        return
      }

      state.sensors[color] = activated

      if (state.playable) {
        if (activated === true) {
          if (state.activationAnimation === null) {
            if (currentVertice.activationSensorId == color) {
              nextActivation()
            }
          }
        } else {
          if (state.activationAnimation) {
            if (currentVertice.activationSensorId == color) {
              nextActivationSequence()
            }
          }
        }
      }
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
    },
    toggleColor (context, {color, activated}) {
      var currentVertice = context.state.vertices[context.state.edges[context.getters.currentActivationEdgeId].getVertice2()]

      context.commit('toggleColor', {currentVertice, color, activated})
    }
  }
})

export default store
