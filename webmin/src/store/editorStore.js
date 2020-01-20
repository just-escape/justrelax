import Vue from 'vue'
import Vuex from 'vuex'
import justRestAPI from '@/store/justRestService.js'
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
      Vue.set(state, 'variables', scenario.variables)
      Vue.set(state, 'rules', scenario.rules)
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
    setVariables (state, variables) {
      Vue.set(state, 'variables', variables)
    },
  },
  actions: {
    loadEditorData(context) {
      context.dispatch('loadTemplates')
    },
    loadTemplates(context) {
      justRestAPI.get('/get_templates/')
        .then(function(response) {
          context.commit('loadTemplates', response.data)
          context.dispatch('loadScenario')
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
    save(context) {
      var formData = new FormData()
      formData.set('scenario_id', 36)
      formData.set('rules', JSON.stringify(context.state.rules))
      formData.set('variables', JSON.stringify(context.state.variables))
      justRestAPI.post('/update_scenario/', formData)
        .then(function(response) {
          notificationStore.dispatch('pushNotification', 'Scenario saved with success!')
          context.commit('loadScenario', response.data)
        })
        .catch(function(error) {
          notificationStore.dispatch('pushError', 'Error while saving scenario: ' + error)
        })
    }
  },
})
