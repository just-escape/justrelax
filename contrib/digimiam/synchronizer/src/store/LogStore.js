import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex);

var store = new Vuex.Store({
  state: {
    logs: [],
    carriageReturns: 0,
    typingLogs: false,
  },
  mutations: {
    // eslint-disable-next-line
    processEventLog (state, {level, message}) {
      state.logs.push({
        level: level,
        message: message,
        displayedMessage: '',
        displayedChars: -1,
      })
      state.carriageReturns += 1
      updateDisplayedMessages()
    },
    lockTypingLogs(state) {
      state.typingLogs = true
    },
    unlockTypingLogs(state) {
      state.typingLogs = false
    },
    typeOneChar(state, logIndex) {
      state.logs[logIndex].displayedChars += 1
      state.logs[logIndex].displayedMessage += state.logs[logIndex].message[state.logs[logIndex].displayedChars]
    },
    typeCarriageReturn(state, logIndex) {
      state.carriageReturns += 1
      state.logs[logIndex].displayedMessage += '<br>'
    }
  },
})

function updateDisplayedMessages() {
  if (store.state.typingLogs === true) {
    return
  }
  store.commit('lockTypingLogs')

  _updateDisplayedMessages()
}

function _updateDisplayedMessages() {
  for (var i = 0 ; i < store.state.logs.length ; i++) {
    if (store.state.logs[i].displayedChars < store.state.logs[i].message.length - 1) {
      store.commit('typeOneChar', i)
      if (store.state.logs[i].level == 'info') {
        if (store.state.logs[i].displayedChars % 29 - 24 == 0) {
          store.commit('typeCarriageReturn', i)
        }
      } else if (store.state.logs[i].level == 'warning') {
        if (store.state.logs[i].displayedChars % 29 - 21 == 0) {
          store.commit('typeCarriageReturn', i)
        }
      }
      setTimeout(_updateDisplayedMessages, 75)
      return
    }
  }

  store.commit('unlockTypingLogs')
}

export default store
