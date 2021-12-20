<template>
  <div class="position-relative">
    <div class="position-absolute price bg-info rounded">{{ price }} {{ $t('nF') }}</div>
    <!-- d-none because the feature has been abandonned -->
    <div v-if="variationSrc" class="d-none position-absolute bg-info rounded" style="height: 21px; bottom: 10px; left: 20px; padding: 0px 2px; opacity: 0.85; filter: drop-shadow(0px 0px 3px rgba(23, 162, 184, 0.75))">
      <img :src="variationSrc" height="17px" width="17px" style="margin-bottom: 4px">
    </div>
    <img :src="src" class="img-fluid">
  </div>
</template>

<script>
import orderStore from '@/store/orderStore.js'

export default {
  name: "OrderSummaryItem",
  computed: {
    variationSrc() {
      return orderStore.state.waffrescoVariations[this.variation]
    },
    src() {
      return orderStore.state.items[this.itemId].imgCart
    },
    price() {
      return orderStore.state.items[this.itemId].price
    },
  },
  props: {
    itemId: String,
    variation: String,
  },
}
</script>

<style scoped>
.price {
  bottom: 10px;
  right: 8px;
  color: white;
  opacity: 0.85;
  filter: drop-shadow(0px 0px 4px rgba(23, 162, 184, 0.75));
  font-size: 0.8rem;
  padding: 1px 5px;
}
</style>
