import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex);

function resetLights(state) {
  for (var i = 0 ; i < state.lights.length ; i++) {
    state.lights[i].validated = false
  }
  state.currentLight = 0
}

export default new Vuex.Store({
  state: {
    lights: [
      {
        color: "darkred",
        activated: false,
        validated: false,
      },
      {
        color: "darkorange",
        activated: false,
        validated: false,
      },
      {
        color: "yellow",
        activated: false,
        validated: false,
      },
      {
        color: "green",
        activated: false,
        validated: false,
      },
      {
        color: "darkturquoise",
        activated: false,
        validated: false,
      },
      {
        color: "dodgerblue",
        activated: false,
        validated: false,
      },
      {
        color: "rebeccapurple",
        activated: false,
        validated: false,
      },
    ],
    currentLight: 0,
    solved: false,
  },
  mutations: {
    processEvent (state, {lightId, activated}) {
      var lightIndex = lightId - 1

      if (state.lights[lightIndex] === undefined) {
        // eslint-disable-next-line
        console.error("Light index " + lightIndex + " does not exist")
        return
      }

      state.lights[lightIndex].activated = activated
      if (lightIndex == state.currentLight) {
        if (activated === true) {
          if (lightIndex == 0 || state.lights[state.currentLight - 1].activated === true) {
            state.lights[lightIndex].validated = true
            state.currentLight += 1
          }
        }
      } else {
        if (activated === true) {
          if (lightIndex > state.currentLight) {
            resetLights(state)
          }
        } else {
          if (lightIndex == state.currentLight - 1) {
            resetLights(state)
          }
        }
      }
    },
  },
})
