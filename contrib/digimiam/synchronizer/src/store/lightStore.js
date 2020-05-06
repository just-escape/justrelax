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
    if (store.state.sensors[store.state.edges[edgeId].activationSensorId] === true) {
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
      '00A': {
        x: 290,
        y: 80,
        rotation: 0,
        color: {
          r: 232,
          g: 62,
          b: 140,
        },
        initColor: {
          r: 232,
          g: 62,
          b: 140,
        },
        glowing: 'glowing',
      },
      '00B': {
        x: 230,
        y: 80,
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
      },
      '00C': {
        x: 260,
        y: 20,
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
      },
      '00D': {
        x: 320,
        y: 20,
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
      },
      '00E': {
        x: 350,
        y: 80,
        rotation: 0,
        color: {
          r: 40,
          g: 167,
          b: 69,
        },
        initColor: {
          r: 40,
          g: 167,
          b: 69,
        },
        glowing: 'glowing',
      },
      '00F': {
        x: 320,
        y: 140,
        rotation: 0,
        color: {
          r: 255,
          g: 193,
          b: 7,
        },
        initColor: {
          r: 255,
          g: 193,
          b: 7,
        },
        glowing: 'glowing',
      },
      '00G': {
        x: 260,
        y: 140,
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
      },
      '01A': {
        x: 290,
        y: 200,
        rotation: 0,
        color: {
          r: 232,
          g: 62,
          b: 140,
        },
        initColor: {
          r: 232,
          g: 62,
          b: 140,
        },
        glowing: 'glowing',
      },
      '01B': {
        x: 230,
        y: 200,
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
      },
      '01E': {
        x: 350,
        y: 200,
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
      },
      '01F': {
        x: 320,
        y: 260,
        rotation: 0,
        color: {
          r: 253,
          g: 126,
          b: 20,
        },
        initColor: {
          r: 253,
          g: 126,
          b: 20,
        },
        glowing: 'glowing',
      },
      '01G': {
        x: 260,
        y: 260,
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
      },
      '02A': {
        x: 290,
        y: 320,
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
      },
      '02B': {
        x: 230,
        y: 320,
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
      },
      '02E': {
        x: 350,
        y: 320,
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
      },
      '02F': {
        x: 320,
        y: 380,
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
      },
      '02G': {
        x: 260,
        y: 380,
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
      },
      '10A': {
        x: 380,
        y: 20,
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
      },
      '10E': {
        x: 440,
        y: 20,
        rotation: 0,
        color: {
          r: 232,
          g: 62,
          b: 140,
        },
        initColor: {
          r: 232,
          g: 62,
          b: 140,
        },
        glowing: 'glowing',
      },
      '10F': {
        x: 410,
        y: 80,
        rotation: 0,
        color: {
          r: 102,
          g: 16,
          b: 242,
        },
        initColor: {
          r: 102,
          g: 16,
          b: 242,
        },
        glowing: 'glowing',
      },
      '11A': {
        x: 380,
        y: 140,
        rotation: 0,
        color: {
          r: 0,
          g: 123,
          b: 255,
        },
        initColor: {
          r: 0,
          g: 123,
          b: 255,
        },
        glowing: 'glowing',
      },
      '11E': {
        x: 440,
        y: 140,
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
      },
      '11F': {
        x: 410,
        y: 200,
        rotation: 0,
        color: {
          r: 40,
          g: 167,
          b: 69,
        },
        initColor: {
          r: 40,
          g: 167,
          b: 69,
        },
        glowing: 'glowing',
      },
      '12A': {
        x: 380,
        y: 260,
        rotation: 0,
        color: {
          r: 255,
          g: 193,
          b: 7,
        },
        initColor: {
          r: 255,
          g: 193,
          b: 7,
        },
        glowing: 'glowing',
      },
      '12E': {
        x: 440,
        y: 260,
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
      },
      '12F': {
        x: 410,
        y: 320,
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
      },
      '13A': {
        x: 380,
        y: 380,
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
      },
      '13E': {
        x: 440,
        y: 380,
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
      },
    },
    edges: {
      '01B-01A': {
        getVertice1: function () {
          return '01B'
        },
        getVertice2: function() {
          return '01A'
        },
        color: 'rgba(255, 255, 255, 0.3)',
        activationPathAnimation: false,
        activated: false,
        validated: false,
        finalAnimation: false,
        getDirection: function() {
          if (store.state.activationSequenceIndex == 0) {
            return 'left-right'
          } else if (store.state.activationSequenceIndex == 1) {
            return 'right-left'
          }
        },
        activationSensorId: 'pink',
      },
      '01A-01F': {
        getVertice1: function() {
          return '01A'
        },
        getVertice2: function() {
          return '01F'
        },
        color: 'rgba(255, 255, 255, 0.3)',
        activationPathAnimation: false,
        activated: false,
        validated: false,
        finalAnimation: false,
        getDirection: function() {
          return 'topleft-bottomright'
        },
        activationSensorId: 'orange',
      },
      '01F-12A': {
        getVertice1: function() {
          return '01F'
        },
        getVertice2: function() {
          return '12A'
        },
        color: 'rgba(255, 255, 255, 0.3)',
        activationPathAnimation: false,
        activated: false,
        validated: false,
        finalAnimation: false,
        getDirection: function() {
          return 'left-right'
        },
        activationSensorId: 'yellow',
      },
      '12A-11F': {
        getVertice1: function() {
          return '12A'
        },
        getVertice2: function() {
          return '11F'
        },
        color: 'rgba(255, 255, 255, 0.3)',
        activationPathAnimation: false,
        activated: false,
        validated: false,
        finalAnimation: false,
        getDirection: function() {
          return 'bottomleft-topright'
        },
        activationSensorId: 'green',
      },
      '11F-11A': {
        getVertice1: function() {
          return '11F'
        },
        getVertice2: function() {
          return '11A'
        },
        color: 'rgba(255, 255, 255, 0.3)',
        activationPathAnimation: false,
        activated: false,
        validated: false,
        finalAnimation: false,
        getDirection: function() {
          return 'bottomright-topleft'
        },
        activationSensorId: 'blue',
      },
      '11A-10F': {
        getVertice1: function() {
          return '11A'
        },
        getVertice2: function() {
          return '10F'
        },
        color: 'rgba(255, 255, 255, 0.3)',
        activationPathAnimation: false,
        activated: false,
        validated: false,
        finalAnimation: false,
        getDirection: function() {
          return 'bottomleft-topright'
        },
        activationSensorId: 'purple',
      },
      '10F-10E': {
        getVertice1: function() {
          return '10F'
        },
        getVertice2: function() {
          return '10E'
        },
        color: 'rgba(255, 255, 255, 0.3)',
        activationPathAnimation: false,
        activated: false,
        validated: false,
        finalAnimation: false,
        getDirection: function() {
          return 'bottomleft-topright'
        },
        activationSensorId: 'pink',
      },
      '01A-00F': {
        getVertice1: function() {
          return '01A'
        },
        getVertice2: function() {
          return '00F'
        },
        color: 'rgba(255, 255, 255, 0.3)',
        activationPathAnimation: false,
        activated: false,
        validated: false,
        finalAnimation: false,
        getDirection: function() {
          if (store.state.activationSequenceIndex == 0) {
            return 'bottomleft-topright'
          } else if (store.state.activationSequenceIndex == 1) {
            return 'topright-bottomleft'
          }
        },
        activationSensorId: null,
      },
      '00F-00E': {
        getVertice1: function() {
          return '00F'
        },
        getVertice2: function() {
          return '00E'
        },
        color: 'rgba(255, 255, 255, 0.3)',
        activationPathAnimation: false,
        activated: false,
        validated: false,
        finalAnimation: false,
        getDirection: function() {
          return 'bottomleft-topright'
        },
        activationSensorId: 'green',
      },
      '00F-00A': {
        getVertice1: function() {
          if (store.state.activationSequenceIndex == 0) {
            return '00F'
          } else if (store.state.activationSequenceIndex == 1) {
            return '00A'
          }
        },
        getVertice2: function() {
          if (store.state.activationSequenceIndex == 0) {
            return '00A'
          } else if (store.state.activationSequenceIndex == 1) {
            return '00F'
          }
        },
        color: 'rgba(255, 255, 255, 0.3)',
        activationPathAnimation: false,
        activated: false,
        validated: false,
        finalAnimation: false,
        getDirection: function() {
          if (store.state.activationSequenceIndex == 0) {
            return 'bottomright-topleft'
          } else if (store.state.activationSequenceIndex == 1) {
            return 'topleft-bottomright'
          }
        },
        activationSensorId: 'yellow',
      },
      '00A-00C': {
        getVertice1: function() {
          if (store.state.activationSequenceIndex == 0) {
            return '00A'
          } else if (store.state.activationSequenceIndex == 1) {
            return '00C'
          }
        },
        getVertice2: function() {
          if (store.state.activationSequenceIndex == 0) {
            return '00C'
          } else if (store.state.activationSequenceIndex == 1) {
            return '00A'
          }
        },
        color: 'rgba(255, 255, 255, 0.3)',
        activationPathAnimation: false,
        activated: false,
        validated: false,
        finalAnimation: false,
        getDirection: function() {
          if (store.state.activationSequenceIndex == 0) {
            return 'bottomright-topleft'
          } else if (store.state.activationSequenceIndex == 1) {
            return 'topleft-bottomright'
          }
        },
        activationSensorId: 'pink',
      },
      '01F-02E': {
        getVertice1: function() {
          return '01F'
        },
        getVertice2: function() {
          return '02E'
        },
        color: 'rgba(255, 255, 255, 0.3)',
        activationPathAnimation: false,
        activated: false,
        validated: false,
        finalAnimation: false,
        getDirection: function() {
          return 'topleft-bottomright'
        },
        activationSensorId: null,
      },
      '02E-02F': {
        getVertice1: function() {
          return '02E'
        },
        getVertice2: function() {
          return '02F'
        },
        color: 'rgba(255, 255, 255, 0.3)',
        activationPathAnimation: false,
        activated: false,
        validated: false,
        finalAnimation: false,
        getDirection: function() {
          return 'topright-bottomleft'
        },
        activationSensorId: null,
      },
      '02E-12F': {
        getVertice1: function() {
          return '02E'
        },
        getVertice2: function() {
          return '12F'
        },
        color: 'rgba(255, 255, 255, 0.3)',
        activationPathAnimation: false,
        activated: false,
        validated: false,
        finalAnimation: false,
        getDirection: function() {
          return 'left-right'
        },
        activationSensorId: null,
      },
      '12F-12E': {
        getVertice1: function() {
          return '12F'
        },
        getVertice2: function() {
          return '12E'
        },
        color: 'rgba(255, 255, 255, 0.3)',
        activationPathAnimation: false,
        activated: false,
        validated: false,
        finalAnimation: false,
        getDirection: function() {
          return 'bottomleft-topright'
        },
        activationSensorId: null,
      },
      '11A-11E': {
        getVertice1: function() {
          return '11A'
        },
        getVertice2: function() {
          return '11E'
        },
        color: 'rgba(255, 255, 255, 0.3)',
        activationPathAnimation: false,
        activated: false,
        validated: false,
        finalAnimation: false,
        getDirection: function() {
          return 'left-right'
        },
        activationSensorId: null,
      },
    },
    activationSequenceIndex: 0,
    activationSequences: [
      {
        edges: [
          '01B-01A',
          '01A-01F',
          '01F-12A',
          '12A-11F',
          '11F-11A',
          '11A-10F',
          '10F-10E',
        ],
      },
      {
        edges: [
          '00A-00C',
          '00F-00A',
          '00F-00E',
        ],
      }
    ],
    sensors: {
      'pink': false,
      'orange': false,
      'yellow': false,
      'green': false,
      'blue': false,
      'purple': false,
    },
    colorDefault: 'rgba(255, 255, 255, 0.3)',
    colorActivation: 'rgba(255, 69, 00, 0.4)',
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
    toggleSensor (state, {activationSequenceEdges, currentActivationEdgeId, sensorId, activated}) {
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
            var firstEdge = state.edges[activationSequenceEdges[0]]

            if (firstEdge.activationSensorId == sensorId) {
              nextActivation()
            }
          }
        } else {
          if (state.activationAnimation) {
            var currentEdgeId = currentActivationEdgeId

            if (state.edges[currentEdgeId].activationSensorId == sensorId) {
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
      var currentActivationEdgeId = context.getters.currentActivationEdgeId
      var activationSequenceEdges = context.getters.activationSequenceEdges

      context.commit('toggleSensor', {activationSequenceEdges, currentActivationEdgeId, sensorId, activated})
    }
  }
})

export default store
