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
      gaufresque: {
        price: 4,
        img: require('@/assets/img/gaufresque.png'),
      },
      potjevleesch: {
        price: 10,
        img: require('@/assets/img/potlevlesch.png'),
      },
      salade_flamande: {
        price: 11,
        img: require('@/assets/img/salade.png'),
      },
      cambraisienne: {
        price: 12,
        img: require('@/assets/img/cambraisienne.png'),
      },
    },
    displayOrderNotification: false,
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
      state.displayOrderNotification = true
      if (!state.hasFirstOrderBeenIssued) {
        state.hasFirstOrderBeenIssued = true
        progressionStore.commit('runMsPepperPantryAfterNotificationAcknowledgement')
      }
    },
    acknowledgeOrderNotification (state) {
      state.displayOrderNotification = false
      if (progressionStore.state.runMsPepperPantryAfterNotificationAcknowledgement) {
        setTimeout(progressionStore.commit, 2000, 'playOverlayVideo', 'ms_pepper_pantry')
      }
    },
  }
})

export default store
