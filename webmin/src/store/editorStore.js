import Vue from 'vue'
import Vuex from 'vuex'
import justRestAPI from '@/store/justRestService.js'
import notificationStore from '@/store/notificationStore.js'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    selectedFQDN: undefined,
    displayedRuleIndex: 0,
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
    iconContextTable: {
      trigger: 'fa-play',
      condition: 'fa-question',
      action: 'fa-exclamation',
    },
    iconTemplateTable: {
      incoming_event: 'fa-sign-in-alt',
      incoming_event_from_node: 'fa-sign-in-alt',
      admin_button_press: 'fa-hand-point-down',
      admin_button_id_press: 'fa-hand-point-down',
      timed_trigger: 'fa-clock',
      periodic_trigger: 'fa-clock',
      timer_trigger: 'fa-clock',
      session_start: 'fa-play',
      session_pause: 'fa-pause',
      session_resume: 'fa-play',
      simple_condition: 'fa-question',
      send_event_string: 'fa-sign-out-alt',
      send_event_object: 'fa-sign-out-alt',
      push_notification: 'fa-users-cog',
      add_record_now: 'fa-users-cog',
      add_record: 'fa-users-cog',
      create_a_new_object: 'fa-file-excel',
      save_object_in_object: 'fa-file-excel',
      save_string_in_object: 'fa-file-excel',
      save_integer_in_object: 'fa-file-excel',
      save_real_in_object: 'fa-file-excel',
      save_boolean_in_object: 'fa-file-excel',
      start_timer: 'fa-clock',
      pause_timer: 'fa-clock',
      resume_timer: 'fa-clock',
      if_then_else_multiple_functions: 'fa-question',
      wait: 'fa-hourglass-start',
      set_variable: 'fa-file-excel',
      trigger_rule: 'fa-cog',
      do_nothing: 'fa-cog',
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
    },
    displayedRule(state) {
      if (state.rules[state.displayedRuleIndex] === undefined) {
        return null
      } else {
        return state.rules[state.displayedRuleIndex]
      }
    },
    selectedRuleIndex(state) {
      if (state.selectedFQDN === undefined) {
        return -1
      } else {
        return state.selectedFQDN[1]
      }
    },
    iconFromContext(state) {
      return (context) => {
        let icon = state.iconContextTable[context]
        if (icon === undefined) {
          return ''
        } else {
          return icon
        }
      }
    },
    iconFromTemplate(state) {
      return (context) => {
        let icon = state.iconTemplateTable[context]
        if (icon === undefined) {
          return ''
        } else {
          return icon
        }
      }
    },
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
    setSelectedFQDN (state, fqdn) {
      state.selectedFQDN = fqdn
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
