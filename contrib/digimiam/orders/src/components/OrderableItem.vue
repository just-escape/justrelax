<template>
  <div
    class="position-relative item media justify-content-end align-items-center w-100"
    :style="'transform: translateX(' + translate + '%)'"
  >
    <div class="media-body text-right">
      <div class="item-title">
        <span class="uppercase">{{ $t(itemId) }}</span>
      </div>
      <div class="size-11 glowing-text mb-1">
        {{ $t(itemId + '_desc') }}
      </div>
      <div class="d-flex flex-row justify-content-end align-items-center">
        <div class="size-11 glowing-text pr-3">{{ price }} {{ $t('Ḟ') }}</div>
        <OrderItemButton @mousedown="$emit('orderMe')" :clickable="orderable && !isRestaurantClosed" :gray="isRestaurantClosed" class="size-11"/>
      </div>
    </div>
    <img :src="src" :width="height + 'px'" class="img-fluid"/>

    <WarningClosed size="small" v-if="isRestaurantClosed"/>
  </div>
</template>

<script>
import OrderItemButton from '@/components/OrderItemButton.vue'
import WarningClosed from '@/components/WarningClosed.vue'
import orderStore from '@/store/orderStore.js'
import progressionStore from '@/store/progressionStore.js'

export default {
  name: "OrderableItem",
  components: {
    OrderItemButton,
    WarningClosed,
  },
  computed: {
    src: function() {
      return orderStore.state.items[this.itemId].img
    },
    price: function() {
      return orderStore.state.items[this.itemId].price
    },
    isRestaurantClosed: function() {
      return progressionStore.state.isRestaurantClosed
    },
  },
  props: {
    itemId: String,
    height: Number,
    translate: Number,
    orderable: Boolean,
  },
}
</script>

<style scoped>
.item {
  /* The property bellow should be used
     in case the current implementation ends up being bugged 
  scroll-snap-align: start;*/
  color: white;
}

.item-title {
  font-size: 1.5rem;
  font-weight: bold;
  filter: drop-shadow(0px 0px 6px rgba(255, 255, 255, 0.75));
}

.uppercase {
  text-transform: uppercase;
}

.glowing-text {
  filter: drop-shadow(0px 0px 1px rgba(255, 255, 255, 0.75));
}
</style>
