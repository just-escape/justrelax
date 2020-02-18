import Vue from 'vue'
import Vuex from 'vuex'
import justRestAPI from '@/store/justRestService.js'
import notificationStore from '@/store/notificationStore.js'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    selectedFQDN: undefined,
    variables: [],
    rules: [],
    templatesByName: {},
    templatesByContext: {
      trigger: [],
      condition: [],
      action: [],
      string: [],
      boolean: [],
      integer: [],
      real: [],
      object: [],
      timer: [],
    },
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
      for (var t of templates) {
        state.templatesByName[t.name] = t
        state.templatesByContext[t.context].push(t)
      }
    },
    loadScenario (state, scenario) {
      Vue.set(state, 'variables', scenario.variables)
      Vue.set(state, 'rules', scenario.rules)
    },
    setDataFromFQDN (state, {fqdn, data}) {
      let copiedFQDN = JSON.parse(JSON.stringify(fqdn))
      let lastFQDNReference = copiedFQDN.pop()
      var dataPath = state
      for (var reference of copiedFQDN) {
        dataPath = dataPath[reference]
      }
      Vue.set(dataPath, lastFQDNReference, data)
    },
    pushDataFromFQDN (state, {fqdn, data}) {
      var dataPath = state
      for (var reference of fqdn) {
        dataPath = dataPath[reference]
      }
      dataPath.push(data)
    },
    addContext (state, context) {
      var args = {}
      for (var link of state.templatesByContext[context][0].links) {
        if (link.type === "argument") {
          args[link.key] = JSON.parse(link.default_value)
        }
      }

      let component = {
        template: state.templatesByContext[context][0].name,
        arguments: args,
      }

      if (context === 'trigger') {
        state.rules[0].content.triggers.push(component)
      } else if (context === 'condition') {
        state.rules[0].content.conditions.push(component)
      } else if (context === 'action') {
        state.rules[0].content.actions.push(component)
      }
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
