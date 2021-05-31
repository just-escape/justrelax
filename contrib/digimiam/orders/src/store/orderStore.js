import Vue from 'vue'
import Vuex from 'vuex'

import publishSubscribeService from './publishSubscribeService'

Vue.use(Vuex)

let store = new Vuex.Store({
  state: {
    credits: 0,
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
        img: require('@/assets/img/potjevleesch.png'),
        imgCart: require('@/assets/img/potjevleesch.png'),
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
    waffrescoVariations: {
      happy: require('@/assets/img/happy.svg'),
      heart: require('@/assets/img/heart.svg'),
      infinite: require('@/assets/img/infinite.svg'),
      konoha: require('@/assets/img/konoha.svg'),
      laughing: require('@/assets/img/laughing.svg'),
      relics: require('@/assets/img/relics.svg'),
      sad: require('@/assets/img/sad.svg'),
      spiral: require('@/assets/img/spiral.svg'),
      star: require('@/assets/img/star.svg'),
      sun: require('@/assets/img/sun.svg'),
      surprised: require('@/assets/img/surprised.svg'),
      triforce: require('@/assets/img/triforce.svg'),
    },
    selectedWaffrescoPatternId: 'happy',
    displayResumeOrderNotification: false,
    displayOrderRecapNotification: false,
    displayEmptyCartHelp: false,
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
    setSelectedWaffrescoPatternId (state, patternId) {
      state.selectedWaffrescoPatternId = patternId
    },
    lockSelectorScroll (state) {
      state.lockSelectorScroll = true
    },
    unlockSelectorScroll (state) {
      state.lockSelectorScroll = false
    },
    displayItemInCart (state, itemId) {
      state.cartItems.unshift(
        {
          itemId: itemId,
          variation: itemId === 'gaufresque' ? state.selectedWaffrescoPatternId : null,
          increment: state.cartItemIncrement++,
        }
      )
    },
    resetOrder (state) {
      state.cartItems = []
    },
    confirmOrder (state) {
      state.displayOrderNotification = true
      if (!state.hasFirstOrderBeenIssued) {
        state.hasFirstOrderBeenIssued = true
        publishSubscribeService.commit('publish', {'category': 'first_order'})
      }
    },
    setDisplayResumeOrderNotification (state, value) {
      state.displayResumeOrderNotification = value
    },
    setDisplayOrderRecapNotification (state, value) {
      state.displayOrderRecapNotification = value
    },
    addItemToCart (state, itemId) {
      state.itemIdToAdd = itemId
      state.addItemToCartSignal = !state.addItemToCartSignal
    },
    setItemOpacity (state, {itemId, opacity}) {
      state.items[itemId].opacity = opacity
    },
    setDisplayEmptyCartHelp (state, value) {
      state.displayEmptyCartHelp = value
    },
    setCredits (state, value) {
      state.credits = value
    },
  }
})

export default store
