<template>
  <div
    class="item media justify-content-end align-items-center w-100"
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
        <div class="size-11 glowing-text pr-3">10 nF</div>
        <OrderItemButton @mousedown="$emit('orderMe')" :disabled="!orderable" class="size-11"/>
      </div>
    </div>
    <img src="@/assets/gaufresque.png" :width="height + 'px'" class="img-fluid"/>
  </div>
</template>

<script>
import OrderItemButton from '@/components/OrderItemButton.vue'
import orderStore from '@/store/orderStore.js'

export default {
  name: "OrderableItem",
  components: {
    OrderItemButton,
  },
  computed: {
    quantity: function() {
      return orderStore.state.items[this.itemId].quantity
    }
  },
  props: ["itemId", "height", "translate", "orderable"],
}
</script>

<style scoped>
.item {
  /*scroll-snap-align: start;*/
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
