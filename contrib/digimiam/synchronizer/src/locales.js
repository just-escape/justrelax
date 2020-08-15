import Vue from 'vue'
import VueI18n from 'vue-i18n'

Vue.use(VueI18n)

const locales = {
  en: {
    warning: 'Warning:',
    info: 'Info:',
    validate: 'VALIDATE',
    dish_generator_matrix: 'DISH GENERATOR MATRIX',
    digimiam_menu: 'DIGIMIAM MENU',
    devices_synchronization: 'DEVICES SYNCHRONIZATION',
    hashtag_hashtag_error: '## Error ##',
    steakfie: 'Steakfie',
    pizzage: 'Pizzage',
    gaufresque: 'Gaufresque',
    puddy_puddy: 'Puddy puddy',
    insectosteak: 'Insectosteak',
    pizzaliere: 'Pizzalière',
    spider_gaufre: 'Spider-gaufre',
    potjevleesch: 'PotjeVleesch',
    protobulle: 'Protobulle',
    cambraisienne: 'Cambraisienne',
    nano_gaufre: 'Nano-gaufre',
    chtite_gelee: 'Ch\'tite gelée',
    salade_flamande: 'Salade Flamande',
    pizzalgue: 'Pizzalgue',
    algaufre: 'Algaufre',
    flubber: 'Flubber',
    danger: 'DANGER',
    toxic_air_detected: 'Toxic air detected',
    immediate_evac: 'Humans are required to evacuate immediately',
  },
  fr: {
    warning: 'Attention:',
    info: 'Info:',
    validate: 'VALIDER',
    dish_generator_matrix: 'MATRICE GÉNÉRATRICE DE PLATS',
    digimiam_menu: 'MENU DU DIGIMIAM',
    devices_synchronization: 'SYNCHRONISATION DES SYSTÈMES',
    hashtag_hashtag_error: '## Erreur ##',
    steakfie: 'Steakfie',
    pizzage: 'Pizzage',
    gaufresque: 'Gaufresque',
    puddy_puddy: 'Puddy puddy',
    insectosteak: 'Insectosteak',
    pizzaliere: 'Pizzalière',
    spider_gaufre: 'Spider-gaufre',
    potjevleesch: 'PotjeVleesch',
    protobulle: 'Protobulle',
    cambraisienne: 'Cambraisienne',
    nano_gaufre: 'Nano-gaufre',
    chtite_gelee: 'Ch\'tite gelée',
    salade_flamande: 'Salade Flamande',
    pizzalgue: 'Pizzalgue',
    algaufre: 'Algaufre',
    flubber: 'Flubber',
    danger: 'DANGER',
    toxic_air_detected: 'Air toxique détecté',
    immediate_evac: 'Évacuation immédiate des humains requise',
  }
}

const i18n = new VueI18n({
  locale: 'fr',
  messages: locales,
})

export default i18n
