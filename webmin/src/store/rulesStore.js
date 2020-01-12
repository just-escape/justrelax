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
    functions: {
      arithmetic: {
        operators: {
          "+": "+",
          "-": "-",
          "*": "*",
          "/": "/",
        }
      },
      comparison: {
        operators: {
          "=": "equals to",
          "!=": "not equals to",
          ">": "greater than",
          ">=": "greater than or equals to",
          "<": "lower than",
          "<=": "lower than or equals to",
        }
      },
      booleanLogic: {
        "and": "and",
        "or": "or",
      },
    }
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
        type: "incoming_message"
      }
      state.rules[ruleIndex].triggers.push(trigger)
    },
    updateTrigger (state, {ruleIndex, trigger}) {
      Vue.set(state.rules[ruleIndex].triggers, trigger.index, trigger)
    },
    addCondition (state, ruleIndex) {
      let condition = {
        index: state.rules[ruleIndex].conditions.length,
        name: "condition 1"
      }
      state.rules[ruleIndex].conditions.push(condition)
    },
    updateCondition (state, {ruleIndex, condition}) {
      Vue.set(state.rules[ruleIndex].conditions, condition.index, condition)
    },
    addAction (state, ruleIndex) {
      let action = {
        index: state.rules[ruleIndex].actions.length,
        name: "action 3"
      }
      state.rules[ruleIndex].actions.push(action)
    },
    updateAction (state, {ruleIndex, action}) {
      Vue.set(state.rules[ruleIndex].actions, action.index, action)
    },
  },
})
