import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    rules: {},
    alarms: {},
    actions: {},
    conditions: {},
    startActions: {},
    resetActions: {},
    admin: {},
  },
  mutations: {
    loadRules (state, rules) {
      state.rules = rules.rules
      state.alarms = rules.alarms
      state.actions = rules.actions
      state.conditions = rules.conditions
      state.startActions = rules.start_actions
      state.resetActions = rules.reset_actions
      state.admin = rules.admin
    }
  },
})
