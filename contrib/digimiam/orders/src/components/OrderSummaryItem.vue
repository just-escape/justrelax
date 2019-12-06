<template>
  <li>
    <div class="d-flex flex-row">
      <div>{{ quantity }} {{ $t(itemId) }}</div>
      <div class="underline-dots flex-grow-1 mx-1"></div>
      <div>{{ price }} nF</div>
    </div>
  </li>
</template>

<script>
import orderStore from '@/store/orderStore.js'

export default {
  name: "OrderSummaryItem",
  computed: {
    quantity: function() {
      return orderStore.state.items[this.itemId].quantity
    },
    price: function() {
      return orderStore.state.items[this.itemId].price * this.quantity
    }
  },
  props: ["itemId"],
}
</script>
