import Vue from 'vue'
import VueI18n from 'vue-i18n'

Vue.use(VueI18n)

const locales = {
  fr: {
    play: 'Jouer',
    run: 'Lancer',
    the: 'la',
    game: 'partie',
    question_mark: '&nbsp;?',
    yes: 'Oui',
    no: 'Non',
    the_digimiam: 'Le Digimiam',
    subtitle: 'L\'Estaminet comme Autrefois',
    meals: 'Les Plats',
    open_the_door: 'Ouvrir la porte',
  },
  en: {
    play: 'Play',
    run: 'Run',
    the: 'the',
    game: 'game',
    question_mark: '?',
    yes: 'Yes',
    no: 'No',
    the_digimiam: 'The Digimiam',
    subtitle: 'Estaminet as in the Olden Days',
    meals: 'Meals',
    open_the_door: 'Open the door',
  },
}

const i18n = new VueI18n({
  locale: 'fr',
  messages: locales,
})

export default i18n
