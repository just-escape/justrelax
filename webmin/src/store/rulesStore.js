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
    },
    contextTypes: {
      trigger: {
        'incoming_message': {
          label: 'Send message',
          contextLinks: [
            {
              type: "text",
              text: "Send message ",
            },
            {
              type: "argument",
              argumentId: "message",
              argument: "hello",
            },
            {
              type: "text",
              text: " to node named ",
            },
            {
              type: "argument",
              argumentId: "node_name",
              argument: "node",
            },
          ],
        },
        'timer_expired': {
          label: 'Timer expired',
          contextLinks: [
            {
              type: "text",
              text: "Once upon a time, ",
            },
            {
              type: "argument",
              argumentId: "story",
              argument: "there was a wolf",
            },
            {
              type: "text",
              text: ", the end",
            }
          ],
        },
        'session_ticked': {
          label: 'Session tick',
          contextLinks: [
            {
              type: "text",
              text: "Once upon a time, ",
            },
            {
              type: "argument",
              argumentId: "story",
              argument: "there was a wolf",
            },
            {
              type: "text",
              text: ", the end",
            }
          ],
        },
        'session_started': {
          label: 'Session started',
          contextLinks: [
            {
              type: "text",
              text: "Once upon a time, ",
            },
            {
              type: "argument",
              argumentId: "story",
              argument: "there was a wolf",
            },
            {
              type: "text",
              text: ", the end",
            }
          ],
        },
        'session_paused': {
          label: 'Session paused',
          contextLinks: [
            {
              type: "text",
              text: "Once upon a time, ",
            },
            {
              type: "argument",
              argumentId: "story",
              argument: "there was a wolf",
            },
            {
              type: "text",
              text: ", the end",
            }
          ],
        },
        'session_resumed': {
          label: 'Session resumed',
          contextLinks: [
            {
              type: "text",
              text: "Once upon a time, ",
            },
            {
              type: "argument",
              argumentId: "story",
              argument: "there was a wolf",
            },
            {
              type: "text",
              text: ", the end",
            }
          ],
        },
      },
      condition: {
        'condition 1': {
          label: 'Boolean comparison',
          contextLinks: [
            {
              type: "argument",
              argumentId: "left",
              argument: true,
            },
            {
              type: "text",
              text: " is // is not ",
            },
            {
              type: "argument",
              argumentId: "right",
              argument: true,
            },
          ],
        },
        'condition 2': {
          label: 'Integer comparison',
          contextLinks: [
            {
              type: "text",
              text: "Once upon a time, ",
            },
            {
              type: "argument",
              argumentId: "story",
              argument: "there was a wolf",
            },
            {
              type: "text",
              text: ", the end",
            }
          ],
        },
        'condition 3': {
          label: 'Real comparison',
          contextLinks: [
            {
              type: "text",
              text: "Once upon a time, ",
            },
            {
              type: "argument",
              argumentId: "story",
              argument: "there was a wolf",
            },
            {
              type: "text",
              text: ", the end",
            }
          ],
        },
        'condition 4': {
          label: 'String comparison',
          contextLinks: [
            {
              type: "text",
              text: "Once upon a time, ",
            },
            {
              type: "argument",
              argumentId: "story",
              argument: "there was a wolf",
            },
            {
              type: "text",
              text: ", the end",
            }
          ],
        },
        'condition 5': {
          label: 'List comparison',
          contextLinks: [
            {
              type: "text",
              text: "Once upon a time, ",
            },
            {
              type: "argument",
              argumentId: "story",
              argument: "there was a wolf",
            },
            {
              type: "text",
              text: ", the end",
            }
          ],
        },
        'condition 6': {
          label: 'Object comparison',
          contextLinks: [
            {
              type: "text",
              text: "Once upon a time, ",
            },
            {
              type: "argument",
              argumentId: "story",
              argument: "there was a wolf",
            },
            {
              type: "text",
              text: ", the end",
            }
          ],
        },
        'condition 7': {
          label: 'Untyped comparison',
          contextLinks: [
            {
              type: "text",
              text: "Once upon a time, ",
            },
            {
              type: "argument",
              argumentId: "story",
              argument: "there was a wolf",
            },
            {
              type: "text",
              text: ", the end",
            }
          ],
        },
        'condition 8': {
          label: 'and',
          contextLinks: [
            {
              type: "text",
              text: "Once upon a time, ",
            },
            {
              type: "argument",
              argumentId: "story",
              argument: "there was a wolf",
            },
            {
              type: "text",
              text: ", the end",
            }
          ],
        },
        'condition 9': {
          label: 'or',
          contextLinks: [
            {
              type: "text",
              text: "Once upon a time, ",
            },
            {
              type: "argument",
              argumentId: "story",
              argument: "there was a wolf",
            },
            {
              type: "text",
              text: ", the end",
            }
          ],
        },
      },
      action: {
        'action 3': {
          label: 'Send message',
          contextLinks: [
            {
              type: "text",
              text: "Send message ",
            },
            {
              type: "argument",
              argumentId: "message",
              argument: "hello",
            },
            {
              type: "text",
              text: " to node named ",
            },
            {
              type: "argument",
              argumentId: "node_name",
              argument: "node",
            },
          ],
        },
        'switch_yellow_led_on': {
          label: 'Integer comparison',
          contextLinks: [
            {
              type: "text",
              text: "Once upon a time, ",
            },
            {
              type: "argument",
              argumentId: "story",
              argument: "there was a wolf",
            },
            {
              type: "text",
              text: ", the end",
            }
          ],
        },
        'cancel_red_and_green_led_hint_alarm': {
          label: 'Real comparison',
          contextLinks: [
            {
              type: "text",
              text: "Once upon a time, ",
            },
            {
              type: "argument",
              argumentId: "story",
              argument: "there was a wolf",
            },
            {
              type: "text",
              text: ", the end",
            }
          ],
        },
      }
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
        type: "incoming_message",
      }
      state.rules[ruleIndex].triggers.push(trigger)
    },
    updateTrigger (state, {ruleIndex, trigger}) {
      Vue.set(state.rules[ruleIndex].triggers, trigger.index, trigger)
    },
    addCondition (state, ruleIndex) {
      let condition = {
        index: state.rules[ruleIndex].conditions.length,
        type: "condition 1",
      }
      state.rules[ruleIndex].conditions.push(condition)
    },
    updateCondition (state, {ruleIndex, condition}) {
      Vue.set(state.rules[ruleIndex].conditions, condition.index, condition)
    },
    addAction (state, ruleIndex) {
      let action = {
        index: state.rules[ruleIndex].actions.length,
        type: "action 3",
      }
      state.rules[ruleIndex].actions.push(action)
    },
    updateAction (state, {ruleIndex, action}) {
      Vue.set(state.rules[ruleIndex].actions, action.index, action)
    },
  },
})
