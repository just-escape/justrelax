import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

var store = new Vuex.Store({
  state: {
    items: {
      salade_flamande: {
        quantity: 0,
        price: 10,
      },
      cambraisienne: {
        quantity: 0,
        price: 10,
      },
      potjevleesch: {
        quantity: 0,
        price: 10,
      },
      frites: {
        quantity: 0,
        price: 10,
      },
      maroilles: {
        quantity: 0,
        price: 10,
      },
      gaufresque: {
        quantity: 0,
        price: 10,
      },
      boisson1: {
        quantity: 0,
        price: 10,
      },
      boisson2: {
        quantity: 0,
        price: 10,
      },
      boisson3: {
        quantity: 0,
        price: 10,
      },
    },
    maxQuantity: 9,
    minQuantity: 0,
  },
  mutations: {
    plusOne (state, itemId) {
      state.items[itemId].quantity = Math.min(state.maxQuantity, state.items[itemId].quantity + 1)
    },
    minusOne (state, itemId) {
      state.items[itemId].quantity = Math.max(state.minQuantity, state.items[itemId].quantity - 1)
    }
  }
})

export default store
