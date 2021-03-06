import Vue from 'vue'
import VueI18n from 'vue-i18n'

Vue.use(VueI18n)

const locales = {
  en: {
    alimentary_data: 'DATA',
    virtual_inventory: 'VIRTUAL INVENTORY',
    ok: 'ok',
    error: 'error',
    temperature: 'Temperature',
    humidity: 'Humidity',
    stocks: 'Stocks',
    kcal_unit: 'kcal',
    h_unit: 'h',
    inhab_unit: 'inhab',
    age: 'age',
    feeling_of_hunger: 'Feeling of hunger (Lille)',
    nutrient_market_rates: 'Nutrient market rates',
    protein: 'prote.',
    lipid: 'lip.',
    carbohydrates: 'carb.',
    vitamin: 'vit.',
    mineral: 'mine.',
    trace_mineral: 'tra.',
    warning: 'Warning:',
    info: 'Info:',
    log: {
      short_info: 'Duis aute irure dolor in reprehenderit.',
      long_info: 'Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.',
      short_warning: 'Cillum dolore eu fugiat nulla pariatur.',
      long_warning: 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.',
    },
    danger: 'DANGER',
    toxic_air_detected: 'Toxic air detected',
    immediate_evac: 'Humans are required to evacuate immediately',
  },
  fr: {
    alimentary_data: 'DONNÉES',
    virtual_inventory: 'INVENTAIRE VIRTUEL',
    ok: 'ok',
    error: 'err.',
    stocks: 'Stocks',
    temperature: 'Température',
    humidity: 'Humidité',
    kcal_unit: 'kcal',
    h_unit: 'h',
    inhab_unit: 'hab',
    age: 'âge',
    feeling_of_hunger: 'Sensation de faim (Lille)',
    nutrient_market_rates: 'Cours des nutriments',
    protein: 'proté.',
    lipid: 'lip.',
    carbohydrates: 'gluc.',
    vitamin: 'vit.',
    mineral: 'miné.',
    trace_mineral: 'oli.',
    warning: 'Attention:',
    info: 'Info:',
    log: {
      waffresco_order: 'Erreur lors de la production de : Gaufresque * 1 (commande G-153-25-59)',
      analysis: 'Analyse de la situation...',
      temperature_control_ok: 'Contrôle de la température : ok',
      humidity_control_ok: 'Contrôle de l\'humidité : ok',
      stocks_control_error: 'Contrôle des stocks alimentaires : erreur',
      nutrients_missing: 'Plusieurs aliments ne sont pas chargés dans leur chambre dédiée',
      human_intervention_required: 'Intervention humaine requise',
      stocks_control_ok: 'Contrôle des stocks alimentaires : ok',
      orders_can_resume: 'Les commandes peuvent à nouveau être produites',
      waiting_customer_validation: 'La commande de Gaufresque * 1 (commande G-153-25-29) est en attente de validation client sur l\'écran de commande',
    },
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
