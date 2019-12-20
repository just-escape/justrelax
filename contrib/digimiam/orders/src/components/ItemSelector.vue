<template>
  <div class="d-flex flex-column justify-content-center">
    <div
      id="meal-container"
      :style="{height: 3 * itemHeight + 'px', overflowY: lockScroll ? 'hidden' : 'scroll'}"
      @scroll="scroll()"
    >
      <OrderableItem
        v-for="(item, itemIndex) in items" :key="item.id"
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
  name: "MealSelector",
  components: {
    OrderableItem,
  },
  data() {
    return {
      mealContainer: undefined,
      lockScroll: false,
      itemHeight: 270,
      items: [
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
          id: "frites",
          translate: 0,
          orderable: false,
        },
        {
          id: "boisson1",
          translate: 0,
          orderable: false,
        },
        {
          id: "boisson2",
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
      if (this.mealContainer.scrollTop == 0) {
        this.items.unshift(this.items.pop())
        this.mealContainer.scrollTop += this.itemHeight
      } else if (this.mealContainer.scrollTop + this.mealContainer.offsetHeight == this.mealContainer.scrollHeight) {
        this.items.push(this.items.shift())
        this.mealContainer.scrollTop -= this.itemHeight
      }

      // With 3 items, the first center position is relative
      // to the first one by an offset of 1
      let firstItem = this.mealContainer.scrollTop / this.itemHeight
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
        targets: this.mealContainer,
        scrollTop: scrollTarget,
        duration: 300,
        easing: 'easeOutQuad',
      })

      setTimeout(this.validateOrder, 2000, this.items[itemIndex].id)
    }
  },
  mounted() {
    this.mealContainer = document.getElementById('meal-container')

    // Doesn't actually scroll, but initialize scroll-related this.items attributes
    this.scroll()
  }
}
</script>

<style scoped>
#meal-container {
  width: 570px;
  height: 294px;
  padding-left: 30px;
  overflow-x: hidden;
  /* scroll-snap-type: y mandatory; */
  -webkit-mask-image: radial-gradient(ellipse 90% 40% at 50% 50%, black 50%, transparent 90%);
}

#meal-container::-webkit-scrollbar {
  display: none;
}
</style>
