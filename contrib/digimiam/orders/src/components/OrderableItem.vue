<template>
  <div
    class="position-relative item media justify-content-end align-items-center w-100"
    :style="'transform: translateX(' + translate + '%)'"
  >
    <div class="media-body text-right">
      <div class="item-title">
        <span class="uppercase">{{ $t(itemId) }}</span>
      </div>
      <div class="glowing-text mb-1">
        {{ $t(itemId + '_desc') }}
      </div>
      <div class="d-flex flex-row justify-content-end align-items-center">
        <div class="glowing-text pr-3">{{ price }} {{ $t('nF') }}</div>
        <OrderItemButton @mousedown="orderMe" :clickable="orderable && !isRestaurantClosed && !showDocumentation" :gray="isRestaurantClosed"/>
      </div>
    </div>
    <img
      :src="src"
      :width="height + 'px'"
      class="transition-02s img-fluid"
      :style="{opacity: opacity, transform: transform}"
    />
    <!-- Conditionning the customizer not only to the fact that a waffresco is displayed, but also to its visibility forces it to be regenerated.
         Otherwise there would be synchronization issues between the 2 waffresco customizers. -->
    <WaffrescoCustomizer
      v-if="itemId === 'gaufresque' && isVisible"
      :clickable="orderable && !isRestaurantClosed && !showDocumentation"
      :gray="isRestaurantClosed"
      :collapseSignal="JSON.stringify([scrollSignal, orderSignal])"
    />

    <WarningClosed size="small" v-if="isRestaurantClosed"/>
  </div>
</template>

<script>
import WaffrescoCustomizer from '@/components/WaffrescoCustomizer.vue'
import OrderItemButton from '@/components/OrderItemButton.vue'
import WarningClosed from '@/components/WarningClosed.vue'
import orderStore from '@/store/orderStore.js'
import progressionStore from '@/store/progressionStore.js'

export default {
  name: "OrderableItem",
  components: {
    OrderItemButton,
    WarningClosed,
    WaffrescoCustomizer,
  },
  data() {
    return {
      scaleX: 1,
      scaleY: 1,
      orderSignal: false,
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
    variation: function() {
      return orderStore.state.items[this.itemId].variation
    },
    showDocumentation: function() {
      return progressionStore.state.showDocumentation
    },
    isRestaurantClosed: function() {
      return progressionStore.state.isRestaurantClosed
    },
    transform: function() {
      return 'scaleX(' + this.scaleX + ') scaleY(' + this.scaleY + ')'
    },
  },
  methods: {
    orderMe() {
      this.orderSignal = !this.orderSignal
      this.$emit('orderMe')
    },
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
    scrollSignal: Boolean,
    isVisible: Boolean,
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
