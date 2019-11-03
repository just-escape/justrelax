import Vue from 'vue'
import VueI18n from 'vue-i18n'

Vue.use(VueI18n)

const locales = {
  en: {
    password: 'PASSWORD',
    this_operation_requires_a_password: 'This operation requires a password',
    continue: 'Continue',
  },
  fr: {
    password: 'MOT DE PASSE',
    this_operation_requires_a_password: 'Cette opération requiert un mot de passe',
    continue: 'Continuer',
  }
}

const i18n = new VueI18n({
  locale: 'fr',
  messages: locales,
})

export default i18n
