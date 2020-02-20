import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

var store = new Vuex.Store({
  state: {
    displayedConfigurationId: "nothing",
    configurations: {
      nothing: [
        [false, false, false],
        [false, false, false],
        [false, false, false]
      ],
      a: [
        [true, false, false],
        [true, false, false],
        [true, false, false]
      ],
      b: [
        [true, false, false],
        [true, true, false],
        [true, false, false]
      ],
      c: [
        [false, false, false],
        [true, false, false],
        [true, true, false]
      ],
      d: [
        [false, false, false],
        [true, true, false],
        [false, true, false]
      ],
      e: [
        [false, true, false],
        [true, true, true],
        [false, true, false]
      ],
      f: [
        [false, false, false],
        [true, true, true],
        [false, true, false]
      ],
      g: [
        [false, true, false],
        [true, true, true],
        [false, false, false]
      ],
      h: [
        [false, true, true],
        [false, true, true],
        [false, false, false]
      ],
    },
  },
  mutations: {
    setDisplayedConfiguration(state, configurationIndex) {
      state.displayedConfigurationId = configurationIndex
    },
  },
})

export default store
