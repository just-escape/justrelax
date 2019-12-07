<template>
  <div class="d-flex flex-column h-100">
    <div class="d-flex flex-row rounded bg-dark shadow-box-dark">
      <Neons class="ml-2"/>
      <h2 class="text-center text-white mx-3 py-1 mb-0">ORDER SUMMARY</h2>
      <Neons class="mr-2"/>
    </div>
    <div class="flex-grow-1 pt-2 px-3">
      <ul class="list-unstyled mb-0">
        <OrderSummaryItem v-for="itemId in cart" :key="itemId.id" :itemId="itemId"/>
      </ul>
    </div>
    <div class="rounded bg-dark text-white px-3 py-1">
      <div class="d-flex flex-row">
        <div>Total</div>
        <div class="underline-dots-white flex-grow-1 mx-1"></div>
        <div>{{ totalPrice }} nF</div>
      </div>
    </div>
  </div>
</template>

<script>
import Neons from '@/components/Neons.vue'
import OrderSummaryItem from '@/components/OrderSummaryItem.vue'
import orderStore from '@/store/orderStore.js'

export default {
  name: "OrderSummary",
  components: {
    Neons,
    OrderSummaryItem,
  },
  computed: {
    cart: function() {
      return Object.keys(orderStore.state.items).filter(
        function(itemId) {
          return orderStore.state.items[itemId].quantity > orderStore.state.minQuantity
        }
      )
    },
    totalPrice: function() {
      var price = 0
      for (var i = 0 ; i < this.cart.length ; i++) {
        price += orderStore.state.items[this.cart[i]].quantity * orderStore.state.items[this.cart[i]].price
      }
      return price
    },
  }
}
</script>

<style scoped>
h2 {
  font-size: 1.2rem;
}
</style>
