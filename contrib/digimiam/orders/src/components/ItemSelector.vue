<template>
  <div class="d-flex flex-column justify-content-center">
    <div
      ref="itemContainer"
      class="item-container"
      :style="{height: 3 * itemHeight + 'px', overflowY: lockScroll ? 'hidden' : 'scroll'}"
      @scroll="scroll()"
    >
      <OrderableItem
        v-for="(item, itemIndex) in items" :key="itemIndex"
        :itemId="item.id"
        :height="itemHeight"
        :translate="item.translate"
        :isVisible="item.isVisible"
        :orderable="item.orderable && !isCartFull && !lockScroll"
        @orderMe="order(itemIndex)"
        :scrollSignal="scrollSignal"
        :style="{'z-index': item.id == 'gaufresque' ? 15: 10}"
      /> <!-- z-index for waffresco pattern selector -->
    </div>
  </div>
</template>

<script>
import OrderableItem from '@/components/OrderableItem.vue'
import orderStore from '@/store/orderStore.js'

export default {
  name: "ItemSelector",
  components: {
    OrderableItem,
  },
  data() {
    return {
      scrollSignal: false,
      itemContainer: undefined,
      itemHeight: 270,
      items: [
        {
          id: "gaufresque",
          translate: 0,
          orderable: true,
          isVisible: false,
        },
        {
          id: "potjevleesch",
          translate: 0,
          orderable: true,
          isVisible: false,
        },
        {
          id: "salade_flamande",
          translate: 0,
          orderable: true,
          isVisible: false,
        },
        {
          id: "cambraisienne",
          translate: 0,
          orderable: true,
          isVisible: false,
        },
        {
          id: "gaufresque",
          translate: 0,
          orderable: true,
          isVisible: false,
        },
        {
          id: "potjevleesch",
          translate: 0,
          orderable: true,
          isVisible: false,
        },
        {
          id: "salade_flamande",
          translate: 0,
          orderable: true,
          isVisible: false,
        },
        {
          id: "cambraisienne",
          translate: 0,
          orderable: true,
          isVisible: false,
        },
      ],
    }
  },
  computed: {
    isCartFull: function() {
      return orderStore.getters.isCartFull
    },
    lockScroll() {
      return orderStore.state.lockSelectorScroll
    },
  },
  methods: {
    scroll: function() {
      this.scrollSignal = !this.scrollSignal

      if (!this.lockScroll) {
        // Ensures infinite scrolling
        if (this.$refs.itemContainer.scrollTop == 0) {
          this.items.unshift(this.items.pop())
          this.$refs.itemContainer.scrollTop += this.itemHeight
        } else if (this.$refs.itemContainer.scrollTop + this.$refs.itemContainer.offsetHeight == this.$refs.itemContainer.scrollHeight) {
          this.items.push(this.items.shift())
          this.$refs.itemContainer.scrollTop -= this.itemHeight
        }
      }

      // With 3 items, the first center position is relative
      // to the first one by an offset of 1
      let firstItem = this.$refs.itemContainer.scrollTop / this.itemHeight
      let centerPosition = firstItem + 1
      for (var i = 0 ; i < this.items.length ; i++) {
        var itemPositionFromCenter = centerPosition - i

        this.items[i].isVisible = itemPositionFromCenter >= -1.5 && itemPositionFromCenter <= 1.5

        // Circular scrolling effect
        this.items[i].translate = Math.abs(itemPositionFromCenter * 15)

        // Order button
        this.items[i].orderable = true
      }
    },
    order: function(itemIndex) {
      orderStore.commit('lockSelectorScroll')
      let scrollTarget = this.itemHeight * (itemIndex - 1)
      this.$anime({
        targets: this.$refs.itemContainer,
        scrollTop: scrollTarget,
        duration: 300,
        easing: 'easeOutQuad',
      })

      orderStore.commit('addItemToCart', this.items[itemIndex].id)
    }
  },
  mounted() {
    // Doesn't actually scroll, but initialize scroll-related this.items attributes
    this.scroll()
  }
}
</script>

<style scoped>
.item-container {
  width: 570px;
  height: 294px;
  padding-left: 30px;
  overflow-x: hidden;
  /* scroll-snap-type: y mandatory; */
  mask-image: radial-gradient(ellipse 90% 40% at 50% 50%, black 50%, transparent 90%);
}

.item-container::-webkit-scrollbar {
  display: none;
}
</style>
