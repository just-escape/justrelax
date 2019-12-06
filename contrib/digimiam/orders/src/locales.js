import Vue from 'vue'
import VueI18n from 'vue-i18n'

Vue.use(VueI18n)

const locales = {
  en: {
    salade_flamande: 'Salade flamande',
    salade_flamande_desc: 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed.',
    cambraisienne: 'Cambraisienne',
    cambraisienne_desc: 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed.',
    potjevleesch: 'PotjeVleesch',
    potjevleesch_desc: 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed.',
    frites: 'Frites',
    frites_desc: 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed.',
    maroilles: 'Maroilles',
    maroilles_desc: 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed.',
    gaufresque: 'Gaufresque',
    gaufresque_desc: 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed.',
    boisson1: 'Boisson 1',
    boisson1_desc: 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed.',
    boisson2: 'Boisson 2',
    boisson2_desc: 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed.',
    boisson3: 'Boisson 3',
    boisson3_desc: 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed.',
  },
  fr: {
    salade_flamande: 'Salade flamande',
    salade_flamande_desc: 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed.',
    cambraisienne: 'Cambraisienne',
    cambraisienne_desc: 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed.',
    potjevleesch: 'PotjeVleesch',
    potjevleesch_desc: 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed.',
    frites: 'Frites',
    frites_desc: 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed.',
    maroilles: 'Maroilles',
    maroilles_desc: 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed.',
    gaufresque: 'Gaufresque',
    gaufresque_desc: 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed.',
    boisson1: 'Boisson 1',
    boisson1_desc: 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed.',
    boisson2: 'Boisson 2',
    boisson2_desc: 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed.',
    boisson3: 'Boisson 3',
    boisson3_desc: 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed.',
  }
}

const i18n = new VueI18n({
  locale: 'fr',
  messages: locales,
})

export default i18n
