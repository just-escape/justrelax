import Vue from 'vue'
import VueI18n from 'vue-i18n'

Vue.use(VueI18n)

const locales = {}

const i18n = new VueI18n({
  locale: 'fr',
  messages: locales,
})

export default i18n
