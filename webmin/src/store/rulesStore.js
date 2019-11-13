import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    rules: [],
    alarms: {},
    actions: {},
    conditions: {},
    startActions: {},
    resetActions: {},
    admin: {},
  },
  mutations: {
    loadRules (state, rules) {
      state.rules = rules
      /*state.alarms = rules.alarms
      state.actions = rules.actions
      state.conditions = rules.conditions
      state.startActions = rules.start_actions
      state.resetActions = rules.reset_actions
      state.admin = rules.admin*/
    },
    addTrigger (state, ruleIndex) {
      let trigger = {
        index: state.rules[ruleIndex].triggers.length,
        type: "hey"
      }
      state.rules[ruleIndex].triggers.push(trigger)
    },
    addCondition (state, ruleIndex) {
      let condition = {
        index: state.rules[ruleIndex].conditions.length,
        name: "new condition"
      }
      state.rules[ruleIndex].conditions.push(condition)
    },
    addAction (state, ruleIndex) {
      let action = {
        index: state.rules[ruleIndex].actions.length,
        name: "new action"
      }
      state.rules[ruleIndex].actions.push(action)

    },
  },
})
