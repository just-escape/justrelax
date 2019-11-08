import Vue from 'vue'
import VueI18n from 'vue-i18n'

Vue.use(VueI18n)

const locales = {
  en: {
    digimiam_food_stocks: 'DIGIMIAM FOOD STOCKS',
    ok: 'ok',
    error: 'error',
    temperature: 'Temp.',
    humidity: 'Humidity',
    stocks: 'Stocks',
    kcal_unit: 'kcal',
    h_unit: 'h',
    inhab_unit: 'inhab',
    age: 'age',
    feeling_of_hunger: 'Feeling of hunger (Lille)',
    nutrient_market_rates: 'Nutrient market rates',
    protein: 'prote.',
    protoid: 'proto.',
    lipid: 'lip.',
    glucid: 'gluc.',
    mineral: 'mine.',
    vitamin: 'vit.',
    antioxidant: 'a-ox.',
    name: 'Name:',
    weight: 'Weight:',
    apple: 'apple',
    orange: 'orange',
    grapes: 'raisins',
    leek: 'leek',
    pear: 'pear',
    lemon: 'lemon',
    strawberry: 'strawberry',
    fish: 'fish',
    protob: 'protob',
    rice: 'rice',
    powder: 'powder',
    pill: 'pill',
    water: 'water',
    milk: 'milk',
    coffee: 'coffee',
    grains: 'grains',
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
    digimiam_food_stocks: 'STOCKS DU DIGIMIAM',
    ok: 'ok',
    error: 'err.',
    stocks: 'Stocks',
    temperature: 'Temp.',
    humidity: 'Humidité',
    kcal_unit: 'kcal',
    h_unit: 'h',
    inhab_unit: 'hab',
    age: 'âge',
    feeling_of_hunger: 'Sensation de faim (Lille)',
    nutrient_market_rates: 'Cours des nutriments',
    protein: 'proté.',
    protoid: 'proto.',
    lipid: 'lip.',
    glucid: 'gluc.',
    mineral: 'miné.',
    vitamin: 'vit.',
    antioxidant: 'a-ox.',
    name: 'Nom:',
    weight: 'Poids:',
    apple: 'pomme',
    orange: 'orange',
    grapes: 'raisin',
    leek: 'poireau',
    pear: 'poire',
    lemon: 'citron',
    strawberry: 'fraise',
    fish: 'poisson',
    protob: 'protob',
    rice: 'riz',
    powder: 'poudre',
    pill: 'pillule',
    water: 'eau',
    milk: 'lait',
    coffee: 'café',
    grains: 'graines',
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
