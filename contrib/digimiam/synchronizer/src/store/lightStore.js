import Vue from 'vue'
import Vuex from 'vuex'

import progressionStore from '@/store/progressionStore.js'
import publishSubscribeService from './publishSubscribeService'

Vue.use(Vuex)

var store = new Vuex.Store({
  state: {
    progression: 30,
    success: false,
    isRestaurantInManualMode: false,
    activatedSensors: {
      red: false,
      white: false,
      pink: false,
      green: false,
      blue: false,
      orange: false,
    },
    sequence: [
      {id: 0, color: "blue", completeness: 0, activable: true},
    ],
    colorSequence: [
      "blue", "orange", "white", "green", "red", "pink", "orange", "green",
      "blue", "white", "red", "blue", "orange", "pink", "blue", "white",
      "orange", "blue", "red", "green", "pink", "blue", "white",
    ],
    sequenceIndex: 0,
  },
  mutations: {
    progress (state, amount) {
      state.progression = Math.max(0, Math.min(100, state.progression + amount))
    },
    setRestaurantInManualMode (state) {
      state.isRestaurantInManualMode = true
    },
    updateCompleteness(state, {sequenceId, deltaCompleteness}) {
      for (let i in state.sequence) {
        if (state.sequence[i].id === sequenceId) {
          state.sequence[i].completeness = Math.max(0, Math.min(100, state.sequence[i].completeness + deltaCompleteness))
          if (state.sequence[i].activable && state.sequence[i].completeness === 100) {
            state.sequence[i].activable = false
            state.progression = Math.min(100, state.progression + 15)

            if (state.progression === 100) {
              state.success = true

              setTimeout(() => {
                for (let s in state.activatedSensors) {
                  state.activatedSensors[s] = false
                }
              }, 1800)
              setTimeout(() => {progressionStore.commit('setLightServiceSuccess')}, 4500)
            }
          }
        }
      }
    },
    next(state) {
      state.sequenceIndex++
      let nextColor = state.success ? "black" : state.colorSequence[state.sequenceIndex % state.colorSequence.length]
      state.sequence = [{id: state.sequenceIndex, color: nextColor, completeness: 0, activable: true}]
    },
    toggleColor (state, {color, activated}) {
      if (activated != state.activatedSensors[color]) {
        publishSubscribeService.commit('publish', {"category": activated ? "on" : "off", "color": color})
      }

      state.activatedSensors[color] = activated
    },
  },
  actions: {
    toggleColor (context, {color, activated}) {
      if (!context.state.isRestaurantInManualMode || progressionStore.state.lightServiceSuccess) {
        return
      }

      context.commit('toggleColor', {color, activated})

      if (color === 'red' || color === 'white') {
        var complementaryColor = 'red'
        if (color === 'red') {
          complementaryColor = 'white'
        }

        let isComplementaryColorActivated = context.state.activatedSensors[complementaryColor]
        let pinkActivation = activated && isComplementaryColorActivated

        // Only notify in case of diff
        if (context.state.activatedSensors.pink !== pinkActivation) {
          context.commit('toggleColor', {color: 'pink', activated: pinkActivation})
        }
      }
    },
  }
})

export default store
