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
    orderedTemplates: [],
  },
  getters: {
    dataFromFQDN(state) {
      return (fqdn) => {
        var data = state
        for (var reference of fqdn) {
          data = data[reference]
        }
        return data
      }
    }
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
    setDataFromFQDN (state, {fqdn, data}) {
      var dataPath = state
      for (var reference of fqdn) {
        dataPath = dataPath[reference]
      }
      dataPath = data
    },
    addComponent (state, {ruleIndex, context}) {
      var args = {}
      for (var link of state.orderedTemplates[context][0].links) {
        if (link.type === "argument") {
          args[link.key] = JSON.parse(link.default_value)
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
    loadEditorData(context, roomId) {
      context.dispatch('loadTemplates', roomId)
    },
    loadTemplates(context, roomId) {
      justRestAPI.get('/get_templates/')
        .then(function(response) {
          context.commit('loadTemplates', response.data)
          context.dispatch('loadScenario', roomId)
        })
        .catch(function(error) {
          notificationStore.dispatch('pushError', 'Error while fetching templates: ' + error)
        })
    },
    loadScenario(context, roomId) {
      justRestAPI.get('/get_scenario/', {params: {room_id: roomId}})
        .then(function(response) {
          context.commit('loadScenario', response.data)
        })
        .catch(function(error) {
          notificationStore.dispatch('pushError', 'Error while fetching scenario: ' + error)
        })
    },
    save(context, roomId) {
      var formData = new FormData()
      formData.append('room_id', roomId)
      formData.append('rules', JSON.stringify(context.state.rules))
      formData.append('variables', JSON.stringify(context.state.variables))
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
