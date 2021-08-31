import Vue from 'vue'
import VueI18n from 'vue-i18n'

Vue.use(VueI18n)

const locales = {
  en: {
    ads: 'ADVERTISEMENTS',
    'gaufresque.mp6': 'gaufresque.mp6',
    'zéphyr_3000 (1).mp6': 'zéphyr_3000 (1).mp6',
    configuration: 'CONFIGURATION',
    mode: 'Mode',
    marmitron: 'Marmitron',
    manual: 'manual',
    security: 'Security',
    on: 'on',
    off: 'off',
    yes: 'yes',
    no: 'no',
    ongoing_maintenance: 'Ongoing maintenance',
    open: 'Open',
    supply: 'Supply',
    food_hydroinflation: 'Food hydroinflation',
    air_quality: 'Air quality',
    optimal: 'Optimal',
    economic: 'Economic',
    danger: 'DANGER',
    toxic_air_detected: 'Toxic air detected',
    immediate_evac: 'Humans are required to evacuate immediately',
    cooking_ai: 'COOKING AI - MARMITRON v0.15',
    services: 'SERVICES',
    lights: 'Lights',
    ventilation: 'Ventilation',
    arm: 'Arm',
    freezer: 'Refrigeration',
    menu: 'Holographic menu',
    stocks: 'Stocks',
    printer: 'Printer',
    oven: 'Oven',
    authentication: 'AUTHENTICATION',
    password_required: 'Opening the network requires the administrator password.',
    forgot_your_password: 'Forgot your password?',
    incorrect_password: 'Incorrect password.',
    confirm: 'CONFIRM',
    cancel: 'CANCEL',
    fallback_authentication: 'FALLBACK AUTHENTICATION',
    fallback_authentication_is_enabled: 'Fallback authentication is enabled. You can authenticate yourself by answering your secret question:',
    what_is_the_secret_ingredient: 'What is the secret ingredient of Digimiam recipes?',
    that_is_not_the_right_answer: 'That is not the right answer.',
  },
  fr: {
    ads: 'PUBLICITÉS',
    'gaufresque.mp6': 'gaufresque.mp6',
    'zéphyr_3000 (1).mp6': 'zéphyr_3000 (1).mp6',
    configuration: 'CONFIGURATION',
    mode: 'Mode',
    marmitron: 'Marmitron',
    manual: 'manuel',
    security: 'Sécurité',
    on: 'activée',
    off: 'désactivée',
    yes: 'oui',
    no: 'non',
    ongoing_maintenance: 'Maintenance en cours',
    open: 'Ouvert',
    supply: 'Approvisionnement',
    food_hydroinflation: 'Hydrogonflage des aliments',
    air_quality: 'Qualité de l\'air',
    optimal: 'Optimal',
    economic: 'Économique',
    danger: 'DANGER',
    toxic_air_detected: 'Air toxique détecté',
    immediate_evac: 'Évacuation immédiate des humains requise',
    cooking_ai: 'INTELLIGENCE CULINAIRE - MARMITRON v0.15',
    services: 'SERVICES',
    lights: 'Lumières',
    ventilation: 'Ventilation',
    arm: 'Bras',
    freezer: 'Réfrigération',
    menu: 'Menu holographique',
    stocks: 'Stocks',
    printer: 'Imprimante',
    oven: 'Four',
    authentication: 'AUTHENTIFICATION',
    password_required: 'L\'ouverture du réseau requiert le mot de passe administrateur.',
    forgot_your_password: 'Mot de passe oublié ?',
    incorrect_password: 'Mot de passe incorrect.',
    confirm: 'VALIDER',
    cancel: 'ANNULER',
    fallback_authentication: 'AUTHENTIFICATION AUXILIAIRE',
    fallback_authentication_is_enabled: 'L\'authentification de secours est activée. Vous pouvez vous authentifier en répondant à votre question secrète :',
    what_is_the_secret_ingredient: 'Quel est l\'ingrédient secret des recettes du Digimiam ?',
    that_is_not_the_right_answer: 'Ce n\'est pas la bonne réponse.',
  },
}

const i18n = new VueI18n({
  locale: 'fr',
  messages: locales,
})

export default i18n
