<template>
  <div class="d-flex flex-column justify-content-center">
    <div
      id="item-container"
      :style="{height: 3 * itemHeight + 'px', overflowY: lockScroll ? 'hidden' : 'scroll'}"
      @scroll="scroll()"
    >
      <OrderableItem
        v-for="(item, itemIndex) in items" :key="itemIndex"
        :itemId="item.id"
        :height="itemHeight"
        :translate="item.translate"
        :orderable="item.orderable && !isCartFull && !lockScroll"
        @orderMe="order(itemIndex)"
      />
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
      itemContainer: undefined,
      lockScroll: false,
      itemHeight: 270,
      items: [
        {
          id: "cambraisienne",
          translate: 0,
          orderable: false,
        },
        {
          id: "gaufresque",
          translate: 0,
          orderable: false,
        },
        {
          id: "potjevleesch",
          translate: 0,
          orderable: false,
        },
        {
          id: "salade_flamande",
          translate: 0,
          orderable: false,
        },
        {
          id: "cambraisienne",
          translate: 0,
          orderable: false,
        },
        {
          id: "gaufresque",
          translate: 0,
          orderable: false,
        },
        {
          id: "potjevleesch",
          translate: 0,
          orderable: false,
        },
        {
          id: "salade_flamande",
          translate: 0,
          orderable: false,
        },
      ]
    }
  },
  computed: {
    isCartFull: function() {
      return orderStore.getters.isCartFull
    },
  },
  methods: {
    scroll: function() {
      // Ensures infinite scrolling
      if (this.itemContainer.scrollTop == 0) {
        this.items.unshift(this.items.pop())
        this.itemContainer.scrollTop += this.itemHeight
      } else if (this.itemContainer.scrollTop + this.itemContainer.offsetHeight == this.itemContainer.scrollHeight) {
        this.items.push(this.items.shift())
        this.itemContainer.scrollTop -= this.itemHeight
      }

      // With 3 items, the first center position is relative
      // to the first one by an offset of 1
      let firstItem = this.itemContainer.scrollTop / this.itemHeight
      let centerPosition = firstItem + 1
      for (var i = 0 ; i < this.items.length ; i++) {
        var itemPositionFromCenter = centerPosition - i

        // Circular scrolling effect
        this.items[i].translate = Math.abs(itemPositionFromCenter * 15)

        // Order button
        if (-0.6 < itemPositionFromCenter && itemPositionFromCenter < 0.6) {
          this.items[i].orderable = true
        } else {
          this.items[i].orderable = false
        }
      }
    },
    lockItemsScroll: function() {
      this.lockScroll = true
    },
    unlockItemsScroll: function() {
      this.lockScroll = false
    },
    validateOrder: function(itemId) {
      orderStore.commit('plusOne', itemId)
      this.unlockItemsScroll()
    },
    order: function(itemIndex) {
      this.lockItemsScroll()
      let scrollTarget = this.itemHeight * (itemIndex - 1)
      this.$anime({
        targets: this.itemContainer,
        scrollTop: scrollTarget,
        duration: 300,
        easing: 'easeOutQuad',
      })

      setTimeout(this.validateOrder, 2000, this.items[itemIndex].id)
    }
  },
  mounted() {
    this.itemContainer = document.getElementById('item-container')

    // Doesn't actually scroll, but initialize scroll-related this.items attributes
    this.scroll()
  }
}
</script>

<style scoped>
#item-container {
  width: 570px;
  height: 294px;
  padding-left: 30px;
  overflow-x: hidden;
  /* scroll-snap-type: y mandatory; */
  mask-image: radial-gradient(ellipse 90% 40% at 50% 50%, black 50%, transparent 90%);
}

#item-container::-webkit-scrollbar {
  display: none;
}
</style>
