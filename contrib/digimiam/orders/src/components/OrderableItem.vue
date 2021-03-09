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
        <div class="size-11 glowing-text pr-3">{{ price }} {{ $t('nF') }}</div>
        <OrderItemButton @mousedown="$emit('orderMe')" :clickable="orderable && !isRestaurantClosed" :gray="isRestaurantClosed" class="size-11"/>
      </div>
    </div>
    <img
      :src="src"
      :width="height + 'px'"
      class="transition-02s img-fluid"
      :style="{opacity: opacity, transform: transform}"
    />

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
  data() {
    return {
      scaleX: 1,
      scaleY: 1,
    }
  },
  computed: {
    src: function() {
      return orderStore.state.items[this.itemId].img
    },
    price: function() {
      return orderStore.state.items[this.itemId].price
    },
    opacity: function() {
      return orderStore.state.items[this.itemId].opacity
    },
    isRestaurantClosed: function() {
      return progressionStore.state.isRestaurantClosed
    },
    transform: function() {
      return 'scaleX(' + this.scaleX + ') scaleY(' + this.scaleY + ')'
    },
  },
  methods: {
    scaleXscaleY1() {
      this.$anime({
        targets: this,
        scaleX: 1,
        scaleY: 1,
        // This timing is related a timing defined in Scene.vue
        duration: 800,
        easing: 'easeOutBounce',
      })
    },
    scaleXscaleY0() {
      this.scaleX = 0
      this.scaleY = 0
      orderStore.commit('setItemOpacity', {itemId: this.itemId, opacity: 1})
    },
  },
  watch: {
    opacity(newValue) {
      if (newValue === 0) {
        // Those timings are related to timings defined in Scene.vue
        setTimeout(this.scaleXscaleY0, 1000)
        setTimeout(this.scaleXscaleY1, 7000)
      }
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

.transition-02s {
  transition: opacity 0.2s;
}
</style>
