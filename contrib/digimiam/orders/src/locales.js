import Vue from 'vue'
import VueI18n from 'vue-i18n'

Vue.use(VueI18n)

const locales = {
  en: {
    nF: 'nF',
    salade_flamande: 'Salade flamande',
    salade_flamande_desc: 'Less carbon, more algae.',
    cambraisienne: 'Cambraisienne',
    cambraisienne_desc: 'An entire pizza compacted in the form of a Bêtise de Cambrai.',
    potjevleesch: 'Potjevlesch',
    potjevleesch_desc: 'A classic revisited with delicate proteins.',
    gaufresque: 'Gaufresque',
    gaufresque_desc: '1000 possible faces to collect!',
    terminal: 'Terminal',
    display_instructions: 'Display instructions',
    unplug_before_intervention: 'Unplug <span class="duct">air ducts</span> before performing the intervention',
    wait_until_sequence_complete: 'Wait for instructions to be completed before performing the intervention',
    all_sequences_are_correct: 'All sequences are correct',
    digimiam_ducts_can_now_be_used: 'Digimiam air ducts can now be used',
    order_matters: 'The order of the instructions must be respected',
    air_ducts: '<span class="duct">Air ducts:</span>',
    air_sources: '<span class="source">Air sources:</span>',
    refectory: '<i class="fas fa-utensils fa-fw"></i>&nbsp;Refectory',
    pantry: '<img src="' + require('@/assets/img/jar_20x16.svg') + '" width="20px" height="16px"></img>&nbsp;Pantry',
    server_room: '<img src="' + require('@/assets/img/server_20x16.svg') + '" width="20px" height="16px"></img>&nbsp;Server room',
    purified_air: '<i class="fa fa-recycle fa-fw"></i>&nbsp;Purified air',
    half_purified_air: '<i class="text-yellow position-absolute fa fa-recycle fa-fw half-left"></i><i class="text-yellow fa fa-biohazard fa-fw half-right"></i>&nbsp;Half-purified air',
    polluted_air: '<i class="text-orange fa fa-biohazard fa-fw"></i>&nbsp;Polluted air',
    sequence_code: 'Color code:',
    sequence_white: '* white: plug the duct to the purified air source',
    sequence_yellow: '* yellow: plug the duct to the half-purified air source',
    sequence_orange: '* orange: plug the duct to the polluted air source',
    sequence_blue: '* blue: plug the duct to a more purified air source',
    sequence_pink: '* pink: apply to this duct the previous instruction',
    sequence_purple: '* purple: apply to this duct the next instruction',
    closed: 'CLOSED',
    cart_full: 'Cart is full',
    confirm_or_reset_order: 'Confirm or reset your order',
    reset_order: 'RESET ORDER',
    confirm_order: 'CONFIRM ORDER',
    total_price: 'Total price',
    empty_cart: 'Empty cart',
    add_an_item: 'Add an item',
    not_enough_credits: 'NOT ENOUGH CREDITS',
    add_credits: 'You can add credits with the authentication module on your right',
    information: 'INFORMATION',
    dear_customers: 'Dear customers,',
    we_are_not_able_to_process_your_order: 'We are not able to process your order for an unknown reason.',
    this_information_has_been_teletransmitted: 'This information has been teletransmitted.',
    ok: 'Ok',
    danger: 'DANGER',
    toxic_air_detected: 'Mustard gas detected',
    immediate_evac: 'Humans are required to evacuate immediately',
    ORDER: 'ORDER',
    "Votre commande est prête !": "Your order is ready!",
    "Production de votre commande en cours.": "Your order is being produced.",
    "Vous pouvez observer son avancement sur votre droite.": "You can observe its progress on your right.",
    "Chers clients,": "Dear customers,",
    "La production de votre commande a été interrompue suite à un incident.": "The production of your order has been interrupted due to an incident.",
    "La situation est maintenant résolue. Nos excuses pour la gêne occasionnée.": "The situation has now been resolved. Our apologies for the inconvenience caused.",
    "Reprendre la commande": "Resume order",
    "Crédits": "Credits",
  },
  fr: {
    nF: 'nF',
    salade_flamande: 'Salade flamande',
    salade_flamande_desc: 'Moins de carbone, plus d\'algues.',
    cambraisienne: 'Cambraisienne',
    cambraisienne_desc: 'Une pizza entière compactée sous forme de bêtise de cambrai.',
    potjevleesch: 'Potjevlesch',
    potjevleesch_desc: 'Un classique revisité aux délicates protéines.',
    gaufresque: 'Gaufresque',
    gaufresque_desc: '1000 visages possibles à collectionner !',
    terminal: 'Terminal',
    display_instructions: 'Lancer les instructions',
    unplug_before_intervention: 'Débranchez les <span class="duct">conduits</span> avant de procéder à l\'intervention',
    wait_until_sequence_complete: 'Attendez la fin des instructions avant de procéder à l\'intervention',
    all_sequences_are_correct: 'Toutes les séquences sont correctes',
    digimiam_ducts_can_now_be_used: 'Les circuits d\'aération du Digimiam sont maintenant pratiquables',
    order_matters: 'L\'ordre des instructions doit être respecté',
    air_ducts: '<span class="duct">Conduits d\'aération :</span>',
    air_sources: '<span class="source">Sources d\'air :</span>',
    refectory: '<i class="fas fa-utensils fa-fw"></i>&nbsp;Réfectoire',
    pantry: '<img src="' + require('@/assets/img/jar_20x16.svg') + '" width="20px" height="16px"></img>&nbsp;Stock alimentaire',
    server_room: '<img src="' + require('@/assets/img/server_20x16.svg') + '" width="20px" height="16px"></img>&nbsp;Salle serveur',
    purified_air: '<i class="fa fa-recycle fa-fw"></i>&nbsp;Air purifié',
    half_purified_air: '<i class="text-yellow position-absolute fa fa-recycle fa-fw half-left"></i><i class="text-yellow fa fa-biohazard fa-fw half-right"></i>&nbsp;Air semi-purifié',
    polluted_air: '<i class="text-orange fa fa-biohazard fa-fw"></i>&nbsp;Air pollué',
    sequence_code: 'Code couleur :',
    sequence_white: '* blanc : brancher le conduit à la source d\'air purifié',
    sequence_yellow: '* jaune : brancher le conduit à la source d\'air semi-purifié',
    sequence_orange: '* orange : brancher le conduit à la source d\'air pollué',
    sequence_blue: '* bleu : brancher le conduit à une source d\'air plus pur',
    sequence_pink: '* rose : appliquer à ce conduit l\'instruction précédente',
    sequence_purple: '* violet : appliquer à ce conduit l\'instruction suivante',
    closed: 'FERMÉ',
    cart_full: 'Panier plein',
    confirm_or_reset_order: 'Validez ou videz le panier',
    reset_order: 'VIDER LE PANIER',
    confirm_order: 'COMMANDER',
    total_price: 'Prix total',
    empty_cart: 'Panier vide',
    add_an_item: 'Ajoutez un article',
    not_enough_credits: 'PAS ASSEZ DE CRÉDITS',
    add_credits: 'Veuillez synchroniser vos crédits grâce au module sur votre droite',
    information: 'INFORMATION',
    dear_customers: 'Chers clients,',
    we_are_not_able_to_process_your_order: 'Nous sommes dans l\'impossibilité de traiter votre commande pour une raison inconnue.',
    this_information_has_been_teletransmitted: 'Cette information a été télétransmise.',
    ok: 'Ok',
    danger: 'DANGER',
    toxic_air_detected: 'Gaz moutarde détecté',
    immediate_evac: 'Évacuation immédiate des humains requise',
    ORDER: 'COMMANDE',
    "Votre commande est prête !": "Votre commande est prête !",
    "Production de votre commande en cours.": "Your order is being produced.",
    "Vous pouvez observer son avancement sur votre droite.": "Vous pouvez observer son avancement sur votre droite.",
    "Chers clients,": "Chers clients,",
    "La production de votre commande a été interrompue suite à un incident.": "La production de votre commande a été interrompue suite à un incident.",
    "La situation est maintenant résolue. Nos excuses pour la gêne occasionnée.": "La situation est maintenant résolue. Nos excuses pour la gêne occasionnée.",
    "Reprendre la commande": "Reprendre la commande",
    "Crédits": "Crédits",
  }
}

const i18n = new VueI18n({
  locale: 'fr',
  messages: locales,
})

export default i18n
