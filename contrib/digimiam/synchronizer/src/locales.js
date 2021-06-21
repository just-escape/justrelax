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
    digimiam_lights: 'DIGIMIAM LIGHTS',
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
    log_lights_have_been_reset: '',
    log_waiting_lights_to_be_resync: 'En attente de la resynchronisation',
  },
  fr: {
    warning: 'Attention:',
    info: 'Info:',
    validate: 'VALIDER',
    dish_generator_matrix: 'MATRICE GÉNÉRATRICE DE PLATS',
    digimiam_menu: 'MENU DU DIGIMIAM',
    digimiam_lights: 'LUMIÈRES DU DIGIMIAM',
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
    log: {
      lights_have_been_reset: 'Réinitialisation complète des lumières',
      waiting_lights_to_be_resync: 'En attente de la resynchronisation',
      pink_was_not_pressed: 'Rose... rose... comment charger le rose ?',
      the_next_light_was_not_pressed: 'La lumière suivante doit être allumée avant que la précédente n\'ait fini d\'être chargée',
      the_light_has_been_turned_off: 'La lumière en cours de chargement a été éteinte avant que la synchronisation ne soit complète',
      too_many_lights_on: 'Il est impossible de charger trop de lumières simultanément',
      light_sync_complete: 'Synchronisation des lumières terminée',
      menu_is_messed_up: 'Réinitialisation complète du menu',
      waiting_dishes_to_be_configured: 'En attente de la reconfiguration des plats du Digimiam',
      dishes_need_to_have_good_prices: 'Le Digimiam ne peut pas se permettre de vendre ces plats à ces prix-là',
      some_dishes_cannot_be_produced: 'Certains plats ne correspondent pas à la carte du Digimiam',
      no_dishes_can_be_produced: 'Aucun de ces plats ne correspond à la carte du Digimiam',
      menu_reconfig_complete: 'Reconfiguration des plats terminée',
      interface_is_not_tactile: 'Les lumières ne peuvent pas être allumées avec l\'écran tactile',
    }
  }
}

const i18n = new VueI18n({
  locale: 'fr',
  messages: locales,
})

export default i18n
