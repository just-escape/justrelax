import Vue from 'vue'
import VueI18n from 'vue-i18n'

Vue.use(VueI18n)

const locales = {
  en: {
    server_room: 'SERVER ROOM',
    high_security_access: 'High-security access',
    alarm: 'ALARM',
    "Intrusion détectée": "Intrusion detected",
    immediate_evac: '<span class="text-red" style="font-weight: bold">Complete</span> evacuation of the room required'
  },
  fr: {
    server_room: 'SALLE SERVEUR',
    high_security_access: 'Accès hautement sécurisé',
    alarm: 'ALARME',
    "Intrusion détectée": "Intrusion détectée",
    immediate_evac: 'Évacuation <span class="text-red" style="font-weight: bold">complète</span> de la salle requise'
  },
}

const i18n = new VueI18n({
  locale: 'fr',
  messages: locales,
})

export default i18n