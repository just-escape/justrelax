import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex);

export default new Vuex.Store({
  state: {
    selectedMeals: [
      {
        name: 'Plat du jour',
        label: null,
        firstComponent: 0,
        secondComponent: 0,
        configuredOnce: false,
      },
      {
        name: 'Plat du jour',
        label: '100% synthétique',
        firstComponent: 0,
        secondComponent: 0,
        configuredOnce: false,
      },
      {
        name: 'Suggestion du Marmitron',
        label: null,
        firstComponent: 0,
        secondComponent: 0,
        configuredOnce: false,
      },
      {
        name: 'Promotion du moment',
        label: null,
        firstComponent: 0,
        secondComponent: 0,
        configuredOnce: false,
      },
    ],
    dishes: [
      ['Steakfie', 'Pizzage', 'Narcicelles', 'Crooquis', 'Gellyme'],
      ['Protoshake', 'Milkshake Haiwaïen', 'Milkenouille', 'Shakie', 'Cubolait'],
      ['Insectosteak', 'Pizzalière', 'Mille pâtes', 'Poukie', 'Dino-ambre'],
      ['Protobulle', 'Pizzule', 'Pastille à la Carbonara', 'Microokie', 'Microgelée'],
      ['Medusa', 'Pizzalgue', 'Sacdenoeud', 'Veggie cookie', ' Flubber'],
    ],
  },
  mutations: {
    onMealSelectionChange: function(state, mealIndex) {
      state.selectedMeals[mealIndex].configuredOnce = true
    }
  },
})
