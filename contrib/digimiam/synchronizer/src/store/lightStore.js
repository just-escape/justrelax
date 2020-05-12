import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex);

function verticesToTurquoise(verticeIds) {
  var targetR = 0
  var targetG = 209
  var targetB = 182

  Vue.prototype.$anime({
    duration: 8000,
    easing: 'easeInQuad',
    update(anim) {
      for (var i = 0 ; i < verticeIds.length ; i++) {
        var verticeId = verticeIds[i]
        var r = store.state.vertices[verticeId].initColor.r - (store.state.vertices[verticeId].initColor.r - targetR) * anim.progress / 100
        var g = store.state.vertices[verticeId].initColor.g - (store.state.vertices[verticeId].initColor.g - targetG) * anim.progress / 100
        var b = store.state.vertices[verticeId].initColor.b - (store.state.vertices[verticeId].initColor.b - targetB) * anim.progress / 100
        store.commit('setVerticeRGB', {verticeId, r, g, b})
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

  for (i = 0 ; i < store.getters.activationSequenceEdges.length ; i++) {
    var v1 = store.state.edges[store.getters.activationSequenceEdges[i]].getVertice1()
    if (!verticeIds.includes(v1)) {
      verticeIds.push(v1)
    }

    var v2 = store.state.edges[store.getters.activationSequenceEdges[i]].getVertice2()
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

function moveGeneratorWire() {
  // TODO: rewrite init animation
  newActivationSequence()
  /*var startY = store.state.generatorWireY

  Vue.prototype.$anime({
    duration: 1200,
    easing: 'linear',
    update: function(anim) {
      var newX = startX - deltaX * anim.progress / 100
      var newY = startY - deltaY * anim.progress / 100

      store.commit('setGeneratorWireY', newY)
    },
    complete: function() {
      var firstEdgeId = store.getters.activationSequenceEdges[0]
      var verticeId = store.state.edges[firstEdgeId].getVertice1()
      var glow = 'glowing-more'
      store.commit('setVerticeGlow', {verticeId, glow})
    }
  })*/
}

function nextDeactivation() {
  var edgeId = store.getters.currentDeactivationEdgeId

  if (edgeId === null) {
    var activationSequenceEdges = store.getters.activationSequenceEdges
    store.commit('resetActivationSequenceEdgesColor', activationSequenceEdges)

    var firstEdgeId = store.getters.activationSequenceEdges[0]
    var verticeId = store.state.edges[firstEdgeId].getVertice1()
    var glow = 'glowing'
    store.commit('setVerticeGlow', {verticeId, glow})

    store.commit('activationSequenceIndexPlusPlus')
    moveGeneratorWire()
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
  if (i < store.getters.activationSequenceEdges.length) {
    var edgeId = store.getters.activationSequenceEdges[i]
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
        },
        initColor: {
          r: 0,
          g: 209,
          b: 182,
        },
        glowing: 'glowing',
        activationSensorId: 'white',
      },
      '12': {
        x: 10 / 4 * 120 - 37.5,
        y: 0 / 2 * 60 * Math.sqrt(3) + 23,
        rotation: 0,
        color: {
          r: 255,
          g: 255,
          b: 255,
        },
        initColor: {
          r: 255,
          g: 255,
          b: 255,
        },
        glowing: 'glowing',
        activationSensorId: 'white',
      },
      '13': {
        x: 12 / 4 * 120 - 37.5,
        y: 0 / 2 * 60 * Math.sqrt(3) + 23,
        rotation: 0,
        color: {
          r: 255,
          g: 255,
          b: 255,
        },
        initColor: {
          r: 255,
          g: 255,
          b: 255,
        },
        glowing: 'glowing',
        activationSensorId: 'white',
      },
      '14': {
        x: 14 / 4 * 120 - 37.5,
        y: 0 / 2 * 60 * Math.sqrt(3) + 23,
        rotation: 0,
        color: {
          r: 255,
          g: 255,
          b: 255,
        },
        initColor: {
          r: 255,
          g: 255,
          b: 255,
        },
        glowing: 'glowing',
        activationSensorId: 'white',
      },
      '15': {
        x: 16 / 4 * 120 - 37.5,
        y: 0 / 2 * 60 * Math.sqrt(3) + 23,
        rotation: 0,
        color: {
          r: 255,
          g: 255,
          b: 255,
        },
        initColor: {
          r: 255,
          g: 255,
          b: 255,
        },
        glowing: 'glowing',
        activationSensorId: 'white',
      },
      '16': {
        x: 18 / 4 * 120 - 37.5,
        y: 0 / 2 * 60 * Math.sqrt(3) + 23,
        rotation: 0,
        color: {
          r: 255,
          g: 255,
          b: 255,
        },
        initColor: {
          r: 255,
          g: 255,
          b: 255,
        },
        glowing: 'glowing',
        activationSensorId: 'white',
      },
      '21': {
        x: 7 / 4 * 120 - 37.5,
        y: 1 / 2 * 60 * Math.sqrt(3) + 23,
        rotation: 0,
        color: {
          r: 0,
          g: 209,
          b: 182,
        },
        initColor: {
          r: 0,
          g: 209,
          b: 182,
        },
        glowing: 'glowing',
        activationSensorId: 'white',
      },
      '22': {
        x: 9 / 4 * 120 - 37.5,
        y: 1 / 2 * 60 * Math.sqrt(3) + 23,
        rotation: 0,
        color: {
          r: 255,
          g: 255,
          b: 255,
        },
        initColor: {
          r: 255,
          g: 255,
          b: 255,
        },
        glowing: 'glowing',
        activationSensorId: 'white',
      },
      '23': {
        x: 11 / 4 * 120 - 37.5,
        y: 1 / 2 * 60 * Math.sqrt(3) + 23,
        rotation: 0,
        color: {
          r: 255,
          g: 255,
          b: 255,
        },
        initColor: {
          r: 255,
          g: 255,
          b: 255,
        },
        glowing: 'glowing',
        activationSensorId: 'white',
      },
      '24': {
        x: 13 / 4 * 120 - 37.5,
        y: 1 / 2 * 60 * Math.sqrt(3) + 23,
        rotation: 0,
        color: {
          r: 255,
          g: 255,
          b: 255,
        },
        initColor: {
          r: 255,
          g: 255,
          b: 255,
        },
        glowing: 'glowing',
        activationSensorId: 'white',
      },
      '25': {
        x: 15 / 4 * 120 - 37.5,
        y: 1 / 2 * 60 * Math.sqrt(3) + 23,
        rotation: 0,
        color: {
          r: 255,
          g: 255,
          b: 255,
        },
        initColor: {
          r: 255,
          g: 255,
          b: 255,
        },
        glowing: 'glowing',
        activationSensorId: 'white',
      },
      '26': {
        x: 17 / 4 * 120 - 37.5,
        y: 1 / 2 * 60 * Math.sqrt(3) + 23,
        rotation: 0,
        color: {
          r: 255,
          g: 255,
          b: 255,
        },
        initColor: {
          r: 255,
          g: 255,
          b: 255,
        },
        glowing: 'glowing',
        activationSensorId: 'white',
      },
      '27': {
        x: 19 / 4 * 120 - 37.5,
        y: 1 / 2 * 60 * Math.sqrt(3) + 23,
        rotation: 0,
        color: {
          r: 255,
          g: 255,
          b: 255,
        },
        initColor: {
          r: 255,
          g: 255,
          b: 255,
        },
        glowing: 'glowing',
        activationSensorId: 'white',
      },
      '31': {
        x: 8 / 4 * 120 - 37.5,
        y: 2 / 2 * 60 * Math.sqrt(3) + 23,
        rotation: 0,
        color: {
          r: 0,
          g: 209,
          b: 182,
        },
        initColor: {
          r: 0,
          g: 209,
          b: 182,
        },
        glowing: 'glowing',
        activationSensorId: 'white',
      },
      '32': {
        x: 10 / 4 * 120 - 37.5,
        y: 2 / 2 * 60 * Math.sqrt(3) + 23,
        rotation: 0,
        color: {
          r: 255,
          g: 255,
          b: 255,
        },
        initColor: {
          r: 255,
          g: 255,
          b: 255,
        },
        glowing: 'glowing',
        activationSensorId: 'white',
      },
      '33': {
        x: 12 / 4 * 120 - 37.5,
        y: 2 / 2 * 60 * Math.sqrt(3) + 23,
        rotation: 0,
        color: {
          r: 255,
          g: 255,
          b: 255,
        },
        initColor: {
          r: 255,
          g: 255,
          b: 255,
        },
        glowing: 'glowing',
        activationSensorId: 'white',
      },
      '34': {
        x: 14 / 4 * 120 - 37.5,
        y: 2 / 2 * 60 * Math.sqrt(3) + 23,
        rotation: 0,
        color: {
          r: 255,
          g: 255,
          b: 255,
        },
        initColor: {
          r: 255,
          g: 255,
          b: 255,
        },
        glowing: 'glowing',
        activationSensorId: 'white',
      },
      '35': {
        x: 16 / 4 * 120 - 37.5,
        y: 2 / 2 * 60 * Math.sqrt(3) + 23,
        rotation: 0,
        color: {
          r: 255,
          g: 255,
          b: 255,
        },
        initColor: {
          r: 255,
          g: 255,
          b: 255,
        },
        glowing: 'glowing',
        activationSensorId: 'white',
      },
      '36': {
        x: 18 / 4 * 120 - 37.5,
        y: 2 / 2 * 60 * Math.sqrt(3) + 23,
        rotation: 0,
        color: {
          r: 255,
          g: 255,
          b: 255,
        },
        initColor: {
          r: 255,
          g: 255,
          b: 255,
        },
        glowing: 'glowing',
        activationSensorId: 'white',
      },
      '41': {
        x: 7 / 4 * 120 - 37.5,
        y: 3 / 2 * 60 * Math.sqrt(3) + 23,
        rotation: 0,
        color: {
          r: 0,
          g: 209,
          b: 182,
        },
        initColor: {
          r: 0,
          g: 209,
          b: 182,
        },
        glowing: 'glowing',
        activationSensorId: 'white',
      },
      '42': {
        x: 9 / 4 * 120 - 37.5,
        y: 3 / 2 * 60 * Math.sqrt(3) + 23,
        rotation: 0,
        color: {
          r: 255,
          g: 255,
          b: 255,
        },
        initColor: {
          r: 255,
          g: 255,
          b: 255,
        },
        glowing: 'glowing',
        activationSensorId: 'white',
      },
      '43': {
        x: 11 / 4 * 120 - 37.5,
        y: 3 / 2 * 60 * Math.sqrt(3) + 23,
        rotation: 0,
        color: {
          r: 255,
          g: 255,
          b: 255,
        },
        initColor: {
          r: 255,
          g: 255,
          b: 255,
        },
        glowing: 'glowing',
        activationSensorId: 'white',
      },
      '44': {
        x: 13 / 4 * 120 - 37.5,
        y: 3 / 2 * 60 * Math.sqrt(3) + 23,
        rotation: 0,
        color: {
          r: 255,
          g: 255,
          b: 255,
        },
        initColor: {
          r: 255,
          g: 255,
          b: 255,
        },
        glowing: 'glowing',
        activationSensorId: 'white',
      },
      '45': {
        x: 15 / 4 * 120 - 37.5,
        y: 3 / 2 * 60 * Math.sqrt(3) + 23,
        rotation: 0,
        color: {
          r: 255,
          g: 255,
          b: 255,
        },
        initColor: {
          r: 255,
          g: 255,
          b: 255,
        },
        glowing: 'glowing',
        activationSensorId: 'white',
      },
      '46': {
        x: 17 / 4 * 120 - 37.5,
        y: 3 / 2 * 60 * Math.sqrt(3) + 23,
        rotation: 0,
        color: {
          r: 255,
          g: 255,
          b: 255,
        },
        initColor: {
          r: 255,
          g: 255,
          b: 255,
        },
        glowing: 'glowing',
        activationSensorId: 'white',
      },
      '47': {
        x: 19 / 4 * 120 - 37.5,
        y: 3 / 2 * 60 * Math.sqrt(3) + 23,
        rotation: 0,
        color: {
          r: 255,
          g: 255,
          b: 255,
        },
        initColor: {
          r: 255,
          g: 255,
          b: 255,
        },
        glowing: 'glowing',
        activationSensorId: 'white',
      },
      '51': {
        x: 8 / 4 * 120 - 37.5,
        y: 4 / 2 * 60 * Math.sqrt(3) + 23,
        rotation: 0,
        color: {
          r: 0,
          g: 209,
          b: 182,
        },
        initColor: {
          r: 0,
          g: 209,
          b: 182,
        },
        glowing: 'glowing',
        activationSensorId: 'white',
      },
      '52': {
        x: 10 / 4 * 120 - 37.5,
        y: 4 / 2 * 60 * Math.sqrt(3) + 23,
        rotation: 0,
        color: {
          r: 255,
          g: 255,
          b: 255,
        },
        initColor: {
          r: 255,
          g: 255,
          b: 255,
        },
        glowing: 'glowing',
        activationSensorId: 'white',
      },
      '53': {
        x: 12 / 4 * 120 - 37.5,
        y: 4 / 2 * 60 * Math.sqrt(3) + 23,
        rotation: 0,
        color: {
          r: 255,
          g: 255,
          b: 255,
        },
        initColor: {
          r: 255,
          g: 255,
          b: 255,
        },
        glowing: 'glowing',
        activationSensorId: 'white',
      },
      '54': {
        x: 14 / 4 * 120 - 37.5,
        y: 4 / 2 * 60 * Math.sqrt(3) + 23,
        rotation: 0,
        color: {
          r: 255,
          g: 255,
          b: 255,
        },
        initColor: {
          r: 255,
          g: 255,
          b: 255,
        },
        glowing: 'glowing',
        activationSensorId: 'white',
      },
      '55': {
        x: 16 / 4 * 120 - 37.5,
        y: 4 / 2 * 60 * Math.sqrt(3) + 23,
        rotation: 0,
        color: {
          r: 255,
          g: 255,
          b: 255,
        },
        initColor: {
          r: 255,
          g: 255,
          b: 255,
        },
        glowing: 'glowing',
        activationSensorId: 'white',
      },
      '56': {
        x: 18 / 4 * 120 - 37.5,
        y: 4 / 2 * 60 * Math.sqrt(3) + 23,
        rotation: 0,
        color: {
          r: 255,
          g: 255,
          b: 255,
        },
        initColor: {
          r: 255,
          g: 255,
          b: 255,
        },
        glowing: 'glowing',
        activationSensorId: 'white',
      },
      '61': {
        x: 7 / 4 * 120 - 37.5,
        y: 5 / 2 * 60 * Math.sqrt(3) + 23,
        rotation: 0,
        color: {
          r: 0,
          g: 209,
          b: 182,
        },
        initColor: {
          r: 0,
          g: 209,
          b: 182,
        },
        glowing: 'glowing',
        activationSensorId: 'white',
      },
      '62': {
        x: 9 / 4 * 120 - 37.5,
        y: 5 / 2 * 60 * Math.sqrt(3) + 23,
        rotation: 0,
        color: {
          r: 255,
          g: 255,
          b: 255,
        },
        initColor: {
          r: 255,
          g: 255,
          b: 255,
        },
        glowing: 'glowing',
        activationSensorId: 'white',
      },
      '63': {
        x: 11 / 4 * 120 - 37.5,
        y: 5 / 2 * 60 * Math.sqrt(3) + 23,
        rotation: 0,
        color: {
          r: 255,
          g: 255,
          b: 255,
        },
        initColor: {
          r: 255,
          g: 255,
          b: 255,
        },
        glowing: 'glowing',
        activationSensorId: 'white',
      },
      '64': {
        x: 13 / 4 * 120 - 37.5,
        y: 5 / 2 * 60 * Math.sqrt(3) + 23,
        rotation: 0,
        color: {
          r: 255,
          g: 255,
          b: 255,
        },
        initColor: {
          r: 255,
          g: 255,
          b: 255,
        },
        glowing: 'glowing',
        activationSensorId: 'white',
      },
      '65': {
        x: 15 / 4 * 120 - 37.5,
        y: 5 / 2 * 60 * Math.sqrt(3) + 23,
        rotation: 0,
        color: {
          r: 255,
          g: 255,
          b: 255,
        },
        initColor: {
          r: 255,
          g: 255,
          b: 255,
        },
        glowing: 'glowing',
        activationSensorId: 'white',
      },
      '66': {
        x: 17 / 4 * 120 - 37.5,
        y: 5 / 2 * 60 * Math.sqrt(3) + 23,
        rotation: 0,
        color: {
          r: 255,
          g: 255,
          b: 255,
        },
        initColor: {
          r: 255,
          g: 255,
          b: 255,
        },
        glowing: 'glowing',
        activationSensorId: 'white',
      },
      '67': {
        x: 19 / 4 * 120 - 37.5,
        y: 5 / 2 * 60 * Math.sqrt(3) + 23,
        rotation: 0,
        color: {
          r: 255,
          g: 255,
          b: 255,
        },
        initColor: {
          r: 255,
          g: 255,
          b: 255,
        },
        glowing: 'glowing',
        activationSensorId: 'white',
      },
      '71': {
        x: 8 / 4 * 120 - 37.5,
        y: 6 / 2 * 60 * Math.sqrt(3) + 23,
        rotation: 0,
        color: {
          r: 0,
          g: 209,
          b: 182,
        },
        initColor: {
          r: 0,
          g: 209,
          b: 182,
        },
        glowing: 'glowing',
        activationSensorId: 'white',
      },
      '72': {
        x: 10 / 4 * 120 - 37.5,
        y: 6 / 2 * 60 * Math.sqrt(3) + 23,
        rotation: 0,
        color: {
          r: 255,
          g: 255,
          b: 255,
        },
        initColor: {
          r: 255,
          g: 255,
          b: 255,
        },
        glowing: 'glowing',
        activationSensorId: 'white',
      },
      '73': {
        x: 12 / 4 * 120 - 37.5,
        y: 6 / 2 * 60 * Math.sqrt(3) + 23,
        rotation: 0,
        color: {
          r: 255,
          g: 255,
          b: 255,
        },
        initColor: {
          r: 255,
          g: 255,
          b: 255,
        },
        glowing: 'glowing',
        activationSensorId: 'white',
      },
      '74': {
        x: 14 / 4 * 120 - 37.5,
        y: 6 / 2 * 60 * Math.sqrt(3) + 23,
        rotation: 0,
        color: {
          r: 255,
          g: 255,
          b: 255,
        },
        initColor: {
          r: 255,
          g: 255,
          b: 255,
        },
        glowing: 'glowing',
        activationSensorId: 'white',
      },
      '75': {
        x: 16 / 4 * 120 - 37.5,
        y: 6 / 2 * 60 * Math.sqrt(3) + 23,
        rotation: 0,
        color: {
          r: 255,
          g: 255,
          b: 255,
        },
        initColor: {
          r: 255,
          g: 255,
          b: 255,
        },
        glowing: 'glowing',
        activationSensorId: 'white',
      },
      '76': {
        x: 18 / 4 * 120 - 37.5,
        y: 6 / 2 * 60 * Math.sqrt(3) + 23,
        rotation: 0,
        color: {
          r: 255,
          g: 255,
          b: 255,
        },
        initColor: {
          r: 255,
          g: 255,
          b: 255,
        },
        glowing: 'glowing',
        activationSensorId: 'white',
      },
    },
    edges: {
      '11-12': {
        getVertice1: function () {
          return '11'
        },
        getVertice2: function() {
          return '12'
        },
        color: 'rgba(255, 255, 255, 0)',
        activationPathAnimation: false,
        activated: false,
        validated: false,
        finalAnimation: false,
        getDirection: function() {
          if (store.state.activationSequenceIndex == 0) {
            return 'left-right'
          } else if (store.state.activationSequenceIndex == 1) {
            return 'left-right'
          }
        },
      },
      '12-13': {
        getVertice1: function() {
          return '12'
        },
        getVertice2: function() {
          return '13'
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
      '13-14': {
        getVertice1: function() {
          return '13'
        },
        getVertice2: function() {
          return '14'
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
      '14-15': {
        getVertice1: function() {
          return '14'
        },
        getVertice2: function() {
          return '15'
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
      '15-16': {
        getVertice1: function() {
          return '15'
        },
        getVertice2: function() {
          return '16'
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
          if (store.state.activationSequenceIndex == 0) {
            return 'left-right'
          } else if (store.state.activationSequenceIndex == 1) {
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
          if (store.state.activationSequenceIndex == 0) {
            return '26'
          } else if (store.state.activationSequenceIndex == 1) {
            return '26'
          }
        },
        getVertice2: function() {
          if (store.state.activationSequenceIndex == 0) {
            return '27'
          } else if (store.state.activationSequenceIndex == 1) {
            return '27'
          }
        },
        color: 'rgba(255, 255, 255, 0)',
        activationPathAnimation: false,
        activated: false,
        validated: false,
        finalAnimation: false,
        getDirection: function() {
          if (store.state.activationSequenceIndex == 0) {
            return 'left-right'
          } else if (store.state.activationSequenceIndex == 1) {
            return 'left-right'
          }
        },
      },
    },
    activationSequenceIndex: 0,
    activationSequences: [
      {
        edges: [
          '11-12',
          '12-13',
          '13-14',
          '14-15',
          '15-16',
        ],
      },
      {
        edges: [
          '21-22',
          '22-23',
          '23-24',
          '24-25',
          '25-26',
          '26-27',
        ],
      }
    ],
    sensors: {
      'white': false,
      'red': false,
      'blue': false,
      'orange': false,
      'green': false,
      'pink': false,
    },
    colorDefault: 'rgba(255, 255, 255, 0)',
    colorActivation: 'rgba(255, 255, 255, 0.3)',
    colorValidated: 'rgba(0, 209, 182, 1)',
    activationAnimation: null,
    playable: true,
  },
  getters: {
    activationSequenceEdges (state) {
      return state.activationSequences[state.activationSequenceIndex].edges
    },
    currentActivationEdgeId (state, getters) {
      for (var i = 0 ; i < getters.activationSequenceEdges.length ; i++) {
        var edgeId = getters.activationSequenceEdges[i]
        var edge = state.edges[edgeId]

        if (!edge.validated) {
          return edgeId
        }
      }

      return null
    },
    currentDeactivationEdgeId (state, getters) {
      for (var i = getters.activationSequenceEdges.length - 1 ; i >= 0 ; i--) {
        var edgeId = getters.activationSequenceEdges[i]
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
    // eslint-disable-next-line
    processEvent (state, {lightId, activated}) {
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
    setVerticeRGB (state, {verticeId, r, g, b}) {
      state.vertices[verticeId].color.r = r
      state.vertices[verticeId].color.g = g
      state.vertices[verticeId].color.b = b
    },
    activationSequenceIndexPlusPlus (state) {
      state.activationSequenceIndex = (state.activationSequenceIndex + 1) % state.activationSequences.length
    },
    setEdgeColor (state, {edgeId, color}) {
      state.edges[edgeId].color = color
    },
    resetActivationSequenceEdgesColor (state, activationSequenceEdges) {
      var white = store.state.colorDefault
      for (var i = 0 ; i < activationSequenceEdges.length ; i++) {
        var edgeId = activationSequenceEdges[i]
        state.edges[edgeId].color = white
      }
    },
    toggleSensor (state, {currentVertice, sensorId, activated}) {
      if (!Object.keys(state.sensors).includes(sensorId)) {
        // eslint-disable-next-line
        console.error("Unknown sensor " + sensorId)
        return
      }

      if (activated !== true && activated !== false) {
        // eslint-disable-next-line
        console.error("Activated must be true or false (received '" + activated + "')")
        return
      }

      state.sensors[sensorId] = activated

      if (state.playable) {
        if (activated === true) {
          if (state.activationAnimation === null) {
            if (currentVertice.activationSensorId == sensorId) {
              nextActivation()
            }
          }
        } else {
          if (state.activationAnimation) {
            if (currentVertice.activationSensorId == sensorId) {
              nextActivationSequence()
            }
          }
        }
      }
    },
  },
  actions: {
    init (context) {
      var firstEdgeId = context.getters.activationSequenceEdges[0]
      var verticeId = store.state.edges[firstEdgeId].getVertice1()
      var glow = 'glowing-more'
      store.commit('setVerticeGlow', {verticeId, glow})

      var color = store.state.colorActivation
      for (var i = 0 ; i < context.getters.activationSequenceEdges.length ; i++) {
        var edgeId = context.getters.activationSequenceEdges[i]
        context.commit('setEdgeColor', {edgeId, color})
      }
    },
    toggleSensor (context, {sensorId, activated}) {
      var currentVertice = context.state.vertices[context.state.edges[context.getters.currentActivationEdgeId].getVertice2()]

      context.commit('toggleSensor', {currentVertice, sensorId, activated})
    }
  }
})

export default store
