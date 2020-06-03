import Vue from 'vue'
import Vuex from 'vuex'

import progressionStore from '@/store/progressionStore.js'

Vue.use(Vuex)

let store = new Vuex.Store({
  state: {
    cartItems: [
      {itemId: 'salade_flamande', increment: -1},
      {itemId: 'salade_flamande', increment: -2},
      {itemId: 'salade_flamande', increment: -3},
      {itemId: 'salade_flamande', increment: -4},
    ],
    cartItemIncrement: 0,
    maxCartItems: 4,
    items: {
      salade_flamande: {
        price: 10,
      },
      cambraisienne: {
        price: 10,
      },
      potjevleesch: {
        price: 10,
      },
      frites: {
        price: 10,
      },
      moules: {
        price: 10,
      },
      gaufresque: {
        price: 10,
      },
      boisson1: {
        price: 10,
      },
      boisson2: {
        price: 10,
      },
      boisson3: {
        price: 10,
      },
      sauce1: {
        price: 0.5,
      },
      sauce2: {
        price: 0.5,
      },
      sauce3: {
        price: 0.5,
      },
      sauce4: {
        price: 0.5,
      },
    },
    displayOrderError: false,
    hasFirstOrderBeenIssued: false,
  },
  getters: {
    isCartFull (state) {
      return state.cartItems.length >= state.maxCartItems
    },
    totalPrice (state) {
      var price = 0
      for (var item of state.cartItems) {
        price += state.items[item.itemId].price
      }
      return price
    },
  },
  mutations: {
    plusOne (state, itemId) {
      state.cartItems.unshift({itemId: itemId, increment: state.cartItemIncrement++})
    },
    resetOrder (state) {
      state.cartItems = []
    },
    confirmOrder (state) {
      state.displayOrderError = true
      if (!state.hasFirstOrderBeenIssued) {
        state.hasFirstOrderBeenIssued = true
        progressionStore.commit('runCutsceneAfterErrorAcknowledgement')
      }
    },
  }
})

export default store
