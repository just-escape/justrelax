import Vue from 'vue'
import Vuex from 'vuex'
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
      incoming_event: 'fas fa-sign-in-alt',
      incoming_event_from_node: 'fas fa-sign-in-alt',
      admin_button_press: 'fas fa-hand-point-down',
      admin_button_id_press: 'fas fa-hand-point-down',
      timed_trigger: 'far fa-clock',
      periodic_trigger: 'far fa-clock',
      timer_trigger: 'far fa-clock',
      session_start: 'fas fa-play',
      session_pause: 'fas fa-pause',
      session_resume: 'fas fa-play',
      node_connected: 'fas fa-link',
      specific_node_connected: 'fas fa-link',
      node_disconnected: 'fas fa-unlink',
      specific_node_disconnected: 'fas fa-unlink',
      simple_condition: 'fas fa-question',
      send_event_string: 'fas fa-sign-out-alt',
      send_event_object: 'fas fa-sign-out-alt',
      push_notification: 'fas fa-users-cog',
      add_record_now: 'fas fa-users-cog',
      add_record: 'fas fa-users-cog',
      create_a_new_object: 'fas fa-file-excel',
      save_object_in_object: 'fas fa-file-excel',
      save_string_in_object: 'fas fa-file-excel',
      save_integer_in_object: 'fas fa-file-excel',
      save_real_in_object: 'fas fa-file-excel',
      save_boolean_in_object: 'fas fa-file-excel',
      start_timer: 'far fa-clock',
      pause_timer: 'far fa-clock',
      resume_timer: 'far fa-clock',
      run_game_session: 'fas fa-play',
      halt_game_session: 'fas fa-pause',
      reset_game_session: 'fas fa-undo-alt',
      if_then_else_multiple_functions: 'fas fa-question',
      wait: 'fas fa-hourglass-start',
      set_variable: 'fas fa-file-excel',
      trigger_rule: 'fas fa-cog',
      do_nothing: 'fas fa-cog',
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
    predfinedChoicesRules(state) {
      var rules = []
      rules.push({rule: null})
      for (var r of state.rules) {
        if (r.id !== undefined) {
          rules.push({rule: r.id})
        }
      }
      return rules
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
    setVariables (state, variables) {
      Vue.set(state, 'variables', variables)
    },
    setSelectedFQDN (state, fqdn) {
      state.selectedFQDN = fqdn
      state.displayedRuleIndex = fqdn[1]
    },
  },
  actions: {
    addComponent (context, contextType) {
      // TODO: Fix this algo
      /**
      // Identify the target FQDN to push the new component
      var fqdn = undefined
      for (var i = context.state.selectedFQDN.length - 1 ; i >= 0 ; i--) {
        if (i <= 3) {
          fqdn = ['rules', context.state.displayedRuleIndex, 'content']

          if (contextType === 'trigger') {
            fqdn.push('triggers')
          } else if (contextType === 'condition') {
            fqdn.push('conditions')
          } else {
            // contextType === 'action'
            fqdn.push('actions')
          }
          break
        } else {
          // Identify the template
          var trimmedFQDN = context.state.selectedFQDN.slice(0, i + 1)
          var trimmedFQDNData = context.getters.dataFromFQDN(trimmedFQDN)
          let dataTemplate = context.state.templatesByName[trimmedFQDNData.template]

          // If the template has context paragraphs...
          if (dataTemplate.context_paragraphs !== undefined) {
            // ... try to find a match
            for (var p of dataTemplate.context_paragraphs) {
              if (p.type === contextType) {
                fqdn = JSON.parse(JSON.stringify(trimmedFQDN))
                fqdn.push('paragraphs')
                fqdn.push(p.key)
                console.log(fqdn)
                console.log(context.state.rules[0].content.actions)
                break
              }
            }

            if (fqdn !== undefined) {
              break // The first for loop
            }
          }
        }
      }*/
      var fqdn = ['rules', context.state.displayedRuleIndex, 'content']

      if (contextType === 'trigger') {
        fqdn.push('triggers')
      } else if (contextType === 'condition') {
        fqdn.push('conditions')
      } else {
        // contextType === 'action'
        fqdn.push('actions')
      }

      // Generate a default component
      var data = {
        template: context.state.templatesByContext[contextType][0].name,
      }

      var args = {}
      for (var link of context.state.templatesByContext[contextType][0].links) {
        if (link.type === "argument") {
          args[link.key] = JSON.parse(link.default_value)
        }
      }

      Vue.set(data, 'arguments', args)

      /* Unlikely to happen, because all default components (index = 0) don't
       * have context paragraphs.
       **/
      if (context.state.templatesByContext[contextType][0].context_paragraphs !== undefined) {
        var paragraphs = {}
        for (var paragraph of context.state.templatesByContext[contextType][0].context_paragraphs) {
          paragraphs[paragraph.key] = []
        }
        Vue.set(data, 'paragraphs', paragraphs)
      }

      context.commit('pushDataFromFQDN', {fqdn, data})
    },
    loadEditorData(context, roomId) {
      context.dispatch('loadTemplates', roomId)
    },
    loadTemplates(context, roomId) {
      Vue.prototype.$justRestAPI.get('/get_templates/')
        .then(function(response) {
          context.commit('loadTemplates', response.data)
          context.dispatch('loadScenario', roomId)
        })
        .catch(function(error) {
          notificationStore.dispatch('pushError', 'Error while fetching templates: ' + error)
        })
    },
    loadScenario(context, roomId) {
      Vue.prototype.$justRestAPI.get('/get_scenario/', {params: {room_id: roomId}})
        .then(function(response) {
          context.commit('loadScenario', response.data)
          if (context.state.rules.length > 0) {
            context.commit('setSelectedFQDN', ['rules', 0])
          }
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
      Vue.prototype.$justRestAPI.post('/update_scenario/', formData)
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
