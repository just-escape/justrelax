import Vue from 'vue'
import VueI18n from 'vue-i18n'

Vue.use(VueI18n)

const locales = {
  en: {
    salade_flamande: 'Salade flamande',
    salade_flamande_desc: 'Lorem ipsum dolor sit amet, consectetur adipiscing elit.',
    cambraisienne: 'Cambraisienne',
    cambraisienne_desc: 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed.',
    potjevleesch: 'PotjeVleesch',
    potjevleesch_desc: 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed.',
    frites: 'Purée de frites',
    frites_desc: 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed.',
    moules: 'Purée de moules salines',
    moules_desc: 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed.',
    gaufresque: 'Gaufresque',
    gaufresque_desc: 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed.',
    boisson1: 'Eau synthétique',
    boisson1_desc: 'Une délicieuse eau reconstituée plus douce que le crystal.',
    boisson2: 'Eau houblonnée',
    boisson2_desc: 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed.',
    boisson3: 'Boisson 3',
    boisson3_desc: 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed.',
    sauce1: 'Poivre',
    sauce2: 'Maroille',
    sauce3: 'Cuivrée',
  },
  fr: {
    salade_flamande: 'Salade flamande',
    salade_flamande_desc: 'Moins de carbone, plus d\'algues.',
    cambraisienne: 'Cambraisienne',
    cambraisienne_desc: 'Une pizza entière compactée sous forme de bêtise de cambrai.',
    potjevleesch: 'PotjeVleesch',
    potjevleesch_desc: 'Un classique revisité aux délicates protéines.',
    frites: 'Purée de frites',
    frites_desc: 'Bien chaude et croustillante.',
    moules: 'Purée de moules salines',
    moules_desc: 'Marinières.',
    gaufresque: 'Gaufresque',
    gaufresque_desc: '1000 visages possibles à collectionner !',
    boisson1: 'Eau synthétique',
    boisson1_desc: 'Une eau reconstituée en provenance d\'usines locales.',
    boisson2: 'Eau houblonnée',
    boisson2_desc: 'Un rafraîchissant aux délicieuses molécules de houblon.',
    boisson3: 'Boisson 3',
    boisson3_desc: 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed.',
    sauce1: 'Poivre',
    sauce2: 'Maroille',
    sauce3: 'Cuivrée',
  }
}

const i18n = new VueI18n({
  locale: 'fr',
  messages: locales,
})

export default i18n
