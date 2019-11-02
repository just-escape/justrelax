import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex);

/* This store exist because vue-moment does not react to locale changes */

var store = new Vuex.Store({
  state: {
    lang: 'fr',
  },
  mutations: {
    setLang(state, lang) {
      if (lang == 'fr' || lang == 'en') {
        state.lang = lang
      } else {
        state.lang = 'en'
      }
    }
  },
})

export default store
