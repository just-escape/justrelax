import Vue from 'vue'
import Vuex from 'vuex'

import progressionStore from '@/store/progressionStore.js'

Vue.use(Vuex)

let store = new Vuex.Store({
  state: {
    lockSelectorScroll: false,
    itemIdToAdd: null,
    addItemToCartSignal: false,
    cartItems: [],
    cartItemIncrement: 0,
    maxCartItems: 4,
    items: {
      gaufresque: {
        price: 4,
        img: require('@/assets/img/gaufresque.png'),
        imgCart: require('@/assets/img/gaufresque.png'),
        opacity: 1,
      },
      potjevleesch: {
        price: 10,
        img: require('@/assets/img/potlevlesch.png'),
        imgCart: require('@/assets/img/potlevlesch.png'),
        opacity: 1,
      },
      salade_flamande: {
        price: 11,
        img: require('@/assets/img/salade.png'),
        imgCart: require('@/assets/img/salade.png'),
        opacity: 1,
      },
      cambraisienne: {
        price: 12,
        img: require('@/assets/img/cambraisienne.png'),
        imgCart: require('@/assets/img/cambraisienne_cart.png'),
        opacity: 1,
      },
    },
    displayOrderNotification: false,
    hasFirstOrderBeenIssued: false,
    orderSomething: false,
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
    lockSelectorScroll (state) {
      state.lockSelectorScroll = true
    },
    unlockSelectorScroll (state) {
      state.lockSelectorScroll = false
    },
    displayItemInCart (state, itemId) {
      state.cartItems.unshift({itemId: itemId, increment: state.cartItemIncrement++})
    },
    resetOrder (state) {
      state.cartItems = []
    },
    confirmOrder (state) {
      state.displayOrderNotification = true
      if (!state.hasFirstOrderBeenIssued) {
        state.hasFirstOrderBeenIssued = true
        progressionStore.commit('runMsPepperStockAfterNotificationAcknowledgement')
      }
    },
    acknowledgeOrderNotification (state) {
      state.displayOrderNotification = false
      if (progressionStore.state.runMsPepperStockAfterNotificationAcknowledgement) {
        setTimeout(progressionStore.commit, 2000, 'playOverlayVideo', 'ms_pepper_stock')
      }
    },
    addItemToCart (state, itemId) {
      state.itemIdToAdd = itemId
      state.addItemToCartSignal = !state.addItemToCartSignal
    },
    setItemOpacity (state, {itemId, opacity}) {
      state.items[itemId].opacity = opacity
    },
  }
})

export default store
