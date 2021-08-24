import Vue from 'vue'
import Vuex from 'vuex'

import progressionStore from '@/store/progressionStore.js'
import publishSubscribeService from './publishSubscribeService'
import lightLogStore from '@/store/lightLogStore.js'

Vue.use(Vuex)

export const EASY = 'easy'
export const NORMAL = 'normal'
export const HARD = 'hard'

var store = new Vuex.Store({
  state: {
    progression: 0,
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
    activatedSensorIds: {},
    sequence: [
      {id: 0, color: "blue", completeness: 0, activable: true},
    ],
    colorSequence: [
      "blue", "orange", "white", "green", "red", "pink", "orange", "green",
      "blue", "white", "red", "blue", "orange", "pink", "blue", "white",
      "orange", "blue", "red", "green", "pink", "blue", "white",
    ],
    sequenceIndex: 0,
    progressionStep: 22,
    isPinkEnabled: false,
    givePinkClueTask: undefined,
    hasPinkClueBeenGiven: false,
    difficulty: NORMAL,
    giveSwitchClueTask: null,
  },
  mutations: {
    setDifficulty(state, difficulty) {
      if ([EASY, NORMAL, HARD].includes(difficulty)) {
        state.difficulty = difficulty
      }

      let currentColor = state.sequence[0].color
      if (difficulty === 'easy') {
        clearTimeout(state.givePinkClueTask)
        state.isPinkEnabled = false
        while (currentColor === 'pink') {
          state.sequenceIndex++
          currentColor = state.colorSequence[state.sequenceIndex % state.colorSequence.length]
        }
        state.sequence = [{id: state.sequenceIndex, color: currentColor, completeness: 0, activable: true}]
      }
    },
    progress (state, amount) {
      state.progression = Math.max(0, Math.min(100, state.progression + amount))

      if (state.progression === 0) {
        state.isPinkEnabled = false
      }
    },
    setRestaurantInManualMode (state) {
      state.isRestaurantInManualMode = true
      state.giveSwitchClueTask = setTimeout(() => store.commit('giveSwitchClue'), 300000)
    },
    giveSwitchClue () {
      lightLogStore.commit('processLog', {logMessage: 'floor_switches_are_idle', level: 'info', useLocale: true})
    },
    updateCompleteness(state, {sequenceId, deltaCompleteness}) {
      for (let i in state.sequence) {
        if (state.sequence[i].id === sequenceId) {
          state.sequence[i].completeness = Math.max(0, Math.min(100, state.sequence[i].completeness + deltaCompleteness))
          if (state.sequence[i].activable && state.sequence[i].completeness === 100) {
            state.sequence[i].activable = false
            state.progression = Math.min(100, state.progression + state.progressionStep)

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
      let nextColor

      if (state.progression > 100 - 2 * state.progressionStep) {
        clearTimeout(state.giveSwitchClueTask)
      }

      if (state.sequence[0].color === 'pink') {
        clearTimeout(state.givePinkClueTask)
      }

      if (state.success) {
        nextColor = 'black'
      } else if (state.difficulty != EASY && !state.isPinkEnabled && state.progression > 100 - 2 * state.progressionStep) {
        // If difficulty allows pink (no pink in EASY mode), force pink the first time the progression is above a certain level
        // Pink is also allowed in further iterations
        state.isPinkEnabled = true
        nextColor = 'pink'
      } else {
        nextColor = state.colorSequence[state.sequenceIndex % state.colorSequence.length]
        if (state.difficulty == EASY || !state.isPinkEnabled) {
          // Pick a non-pink color if difficulty does not allow pink or if pink is not yet allowed
          while (nextColor === 'pink') {
            state.sequenceIndex++
            nextColor = state.colorSequence[state.sequenceIndex % state.colorSequence.length]
          }
        } else {
          if (state.sequence[0].color === 'pink') {
            // We don't want pink twice in a row
            while (nextColor === 'pink') {
              state.sequenceIndex++
              nextColor = state.colorSequence[state.sequenceIndex % state.colorSequence.length]
            }
          }
        }
      }

      if (nextColor === 'pink') {
        state.givePinkClueTask = setTimeout(store.commit, 45000, 'givePinkClue')
      }

      state.sequence = [{id: state.sequenceIndex, color: nextColor, completeness: 0, activable: true}]
    },
    givePinkClue(state) {
      if (!state.hasPinkClueBeenGiven) {
        state.hasPinkClueBeenGiven = true
        lightLogStore.commit('processLog', {logMessage: 'pink_clue', level: 'info', useLocale: true})
      }
    },
    // eslint-disable-next-line
    toggleColor (state, {color, id, activated}) {
      if (activated != state.activatedSensors[color]) {
        publishSubscribeService.commit('publish', {"category": activated ? "on" : "off", "color": color})
      }

      state.activatedSensors[color] = activated
      if (activated) {
        Vue.set(state.activatedSensorIds, id, color)
      } else {
        state.activatedSensorIds = Object.fromEntries(Object.entries(state.activatedSensorIds).map(([key, value]) => [key, value == color ? undefined : value]))
      }
    },
  },
  actions: {
    toggleColor (context, {color, id, activated}) {
      if (!context.state.isRestaurantInManualMode || progressionStore.state.lightServiceSuccess) {
        return
      }

      context.commit('toggleColor', {color, id, activated})

      if (color === 'red' || color === 'white') {
        var complementaryColor = 'red'
        if (color === 'red') {
          complementaryColor = 'white'
        }

        let isComplementaryColorActivated = context.state.activatedSensors[complementaryColor]
        let pinkActivation = activated && isComplementaryColorActivated

        // Only notify in case of diff
        if (context.state.activatedSensors.pink !== pinkActivation) {
          context.commit('toggleColor', {color: 'pink', id: -1, activated: pinkActivation})
        }
      }
    },
  }
})

export default store
