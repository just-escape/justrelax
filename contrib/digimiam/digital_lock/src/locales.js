import Vue from 'vue'
import VueI18n from 'vue-i18n'

Vue.use(VueI18n)

const locales = {
  en: {
    server_room: 'SERVER ROOM',
    high_security_access: 'High-security access', 
  },
  fr: {
    server_room: 'SALLE SERVEUR',
    high_security_access: 'Accès hautement sécurisé',
  },
}

const i18n = new VueI18n({
  locale: 'fr',
  messages: locales,
})

export default i18n