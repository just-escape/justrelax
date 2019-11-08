import Vue from 'vue'
import Vuex from 'vuex'

import i18n from '@/locales.js'

Vue.use(Vuex)

var store = new Vuex.Store({
  state: {
    fr: {
      logs: [],
      typingLogs: false,
    },
    en: {
      logs: [],
      typingLogs: false,
    },
  },
  mutations: {
    processLog (state, log) {
      for (var i = 0 ; i < Object.keys(state).length ; i++) {
        var lang = Object.keys(state)[i]

        state[lang].logs.push({
          level: log.level,
          message: i18n.t('log.' + log.locale, lang),
          displayedMessage: '',
          displayedChars: -1,
        })
        state[lang].carriageReturns += 1
        updateDisplayedMessages(lang)
      }
    },
    lockTypingLogs(state, lang) {
      state[lang].typingLogs = true
    },
    unlockTypingLogs(state, lang) {
      state[lang].typingLogs = false
    },
    typeOneChar(state, {lang, logIndex}) {
      state[lang].logs[logIndex].displayedChars += 1
      state[lang].logs[logIndex].displayedMessage += state[lang].logs[logIndex].message[state[lang].logs[logIndex].displayedChars]
    },
  },
})

function updateDisplayedMessages(lang) {
  if (store.state[lang].typingLogs === true) {
    return
  }
  store.commit('lockTypingLogs', lang)

  _updateDisplayedMessages(lang)
}

function _updateDisplayedMessages(lang) {
  for (var i = 0 ; i < store.state[lang].logs.length ; i++) {
    if (store.state[lang].logs[i].displayedChars < store.state[lang].logs[i].message.length - 1) {
      var logIndex = i
      store.commit('typeOneChar', {lang, logIndex})
      setTimeout(_updateDisplayedMessages, 75, lang)
      return
    }
  }

  store.commit('unlockTypingLogs', lang)
}

export default store
