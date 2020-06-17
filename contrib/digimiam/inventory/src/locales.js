import Vue from 'vue'
import VueI18n from 'vue-i18n'

Vue.use(VueI18n)

const locales = {
  en: {
    alimentary_statistics: 'ALIMENTARY STATISTICS',
    stock_management: 'STOCK MANAGEMENT',
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
  },
  fr: {
    alimentary_statistics: 'STATISTIQUES ALIMENTAIRES',
    stock_management: 'GESTION DES STOCKS',
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
      short_info: 'Cillum dolore eu fugiat nulla pariatur.',
      long_info: 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.',
      short_warning: 'Duis aute irure dolor in reprehenderit.',
      long_warning: 'Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.',
    },
  }
}

const i18n = new VueI18n({
  locale: 'fr',
  messages: locales,
})

export default i18n
