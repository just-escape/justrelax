import Vue from 'vue'
import VueI18n from 'vue-i18n'

Vue.use(VueI18n)

const locales = {
  fr: {
    easy: 'Facile',
    normal: 'Normal',
    hard: 'Difficile',
    play: 'Jouer',
    in: 'en',
    question_mark: '&nbsp;?',
    yes: 'Oui',
    no: 'Non',
    the_digimiam: 'Le Digimiam',
    subtitle: 'L\'Estaminet comme Autrefois',
    meals: 'Les Plats',
    open_the_door: 'Ouvrir la porte',
  },
  en: {
    easy: 'Easy',
    normal: 'Normal',
    hard: 'Hard',
    play: 'Play',
    in: 'in',
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
