import Vue from 'vue'
import Vuex from 'vuex'
import justRestAPI from '@/store/justRestService2.js'
import notificationStore from '@/store/notificationStore.js'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    variables: [],
    rules: [],
    functions: {},
    orderedFunctions: [],
    contextTypes: {
      trigger: {},
      condition: {},
      action: {},
    },
    orderedContextTypes: {},
  },
  mutations: {
    loadFixtures (state, fixtures) {
      var i

      state.orderedFunctions = fixtures.functions
      for (i = 0 ; i < state.orderedFunctions.length ; i++) {
        state.functions[state.orderedFunctions[i].name] = state.orderedFunctions[i]
      }

      state.orderedContextTypes.trigger = fixtures.trigger_types
      for (i = 0 ; i < state.orderedContextTypes.trigger.length ; i++) {
        state.contextTypes.trigger[state.orderedContextTypes.trigger[i].name] = state.orderedContextTypes.trigger[i]
      }

      state.orderedContextTypes.condition = fixtures.condition_types
      for (i = 0 ; i < state.orderedContextTypes.condition.length ; i++) {
        state.contextTypes.condition[state.orderedContextTypes.condition[i].name] = state.orderedContextTypes.condition[i]
      }

      state.orderedContextTypes.action = fixtures.action_types
      for (i = 0 ; i < state.orderedContextTypes.action.length ; i++) {
        state.contextTypes.action[state.orderedContextTypes.action[i].name] = state.orderedContextTypes.action[i]
      }
    },
    loadScenario (state, scenario) {
      state.rules = scenario.rules
      state.variables = scenario.variables
    },
    addRule (state) {
      state.rules.push(
        {
          triggers: [],
          conditions: [],
          actions: [],
          name: "Rule " + (state.rules.length + 1),
        }
      )
    },
    addTrigger (state, ruleIndex) {
      var values = {}
      let links = state.orderedContextTypes.trigger[0].links
      for (var i = 0 ; i < links.length ; i++) {
        if (links[i].link_type === "argument") {
          values[links[i].key] = links[i].default_value
        }
      }

      let trigger = {
        content_type: state.orderedContextTypes.trigger[0].name,
        arguments: values,
      }

      state.rules[ruleIndex].triggers.push(trigger)
    },
    updateTrigger (state, {ruleIndex, triggerIndex, trigger}) {
      Vue.set(state.rules[ruleIndex].triggers, triggerIndex, trigger)
    },
    addCondition (state, ruleIndex) {
      var values = {}
      let links = state.orderedContextTypes.condition[0].links
      for (var i = 0 ; i < links.length ; i++) {
        if (links[i].link_type === "argument") {
          values[links[i].key] = links[i].default_value
        }
      }

      let condition = {
        content_type: state.orderedContextTypes.condition[0].name,
        arguments: values,
      }

      state.rules[ruleIndex].conditions.push(condition)
    },
    updateCondition (state, {ruleIndex, conditionIndex, condition}) {
      Vue.set(state.rules[ruleIndex].conditions, conditionIndex, condition)
    },
    addAction (state, ruleIndex) {
      var values = {}
      let links = state.orderedContextTypes.action[0].links
      for (var i = 0 ; i < links.length ; i++) {
        if (links[i].link_type === "argument") {
          values[links[i].key] = links[i].default_value
        }
      }

      let action = {
        content_type: state.orderedContextTypes.action[0].name,
        arguments: values,
      }

      state.rules[ruleIndex].actions.push(action)
    },
    updateAction (state, {ruleIndex, actionIndex, action}) {
      Vue.set(state.rules[ruleIndex].actions, actionIndex, action)
    },
  },
  actions: {
    loadFixtures(context) {
      justRestAPI.get('/get_fixtures/')
        .then(function(response) {
          context.commit('loadFixtures', response.data)
        })
        .catch(function(error) {
          notificationStore.dispatch('pushError', 'Error while fetching fixtures: ' + error)
        })
    },
    loadScenario(context) {
      justRestAPI.get('/get_scenario/', {
        params: {
          scenario_id: 36,
        },
      })
        .then(function(response) {
          context.commit('loadScenario', response.data)
        })
        .catch(function(error) {
          notificationStore.dispatch('pushError', 'Error while fetching scenario: ' + error)
        })
    },
  },
})
