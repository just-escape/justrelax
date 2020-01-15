import Vue from 'vue'
import Vuex from 'vuex'
import justRestAPI from '@/store/justRestService2.js'
import notificationStore from '@/store/notificationStore.js'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    variables: [],
    rules: [],
    templates: {
      function: {},
      trigger: {},
      condition: {},
      action: {},
    },
    orderedTemplates: {},
  },
  mutations: {
    loadTemplates (state, templates) {
      for (var context of ['function', 'trigger', 'condition', 'action']) {
        state.orderedTemplates[context] = templates[context]
        for (var template of state.orderedTemplates[context]) {
          state.templates[context][template.name] = template
        }
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
    addComponent (state, {ruleIndex, context}) {
      var args = {}
      for (var link of state.orderedTemplates[context][0].links) {
        if (link.type === "argument") {
          args[link.key] = link.default_value
        }
      }

      let component = {
        template: state.orderedTemplates[context][0].name,
        arguments: args,
      }

      // + 's' is dirty
      state.rules[ruleIndex][context + 's'].push(component)
    },
    updateComponent (state, {ruleIndex, context, componentIndex, component}) {
      // + 's' is dirty
      Vue.set(state.rules[ruleIndex][context + 's'], componentIndex, component)
    },
  },
  actions: {
    loadTemplates(context) {
      justRestAPI.get('/get_templates/')
        .then(function(response) {
          context.commit('loadTemplates', response.data)
        })
        .catch(function(error) {
          notificationStore.dispatch('pushError', 'Error while fetching templates: ' + error)
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
