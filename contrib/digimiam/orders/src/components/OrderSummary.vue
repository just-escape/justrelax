<template>
  <div class="position-relative d-flex flex-column flex-grow-1">
    <OrderNotification class="position-absolute" :displayed="displayOrderNotification" @ok="acknowledgeNotification"/>

    <div class="overflow-hidden p-4">
      <div class="d-flex flex-row justify-content-end align-items-end mb-2 px-2">
        <div class="text-orange text-right pr-3" :class="{'d-none': !isCartFull}">
          <div class="font-weight-bold"> {{ $t('cart_full') }}</div>
          <div class="small">{{ $t('confirm_or_reset_order') }}</div>
        </div>
        <div class="w-50">
          <b-btn
            block
            :variant="isRestaurantClosed ? 'outline-secondary' : 'outline-info'"
            class="py-2"
            :disabled="!cartItems.length || isRestaurantClosed"
            :style="{opacity: !cartItems.length || isRestaurantClosed ? 0.4 : 1}"
            @click="reset"
          >
            {{ $t('reset_order') }}
          </b-btn>
        </div>
      </div>

      <div class="d-flex flex-row justify-content-end align-items-center mb-4 px-2">
        <div class="text-white pr-3">
          <div class="d-flex flex-row font-weight-bold">
            <div>{{ $t('total') }} {{ totalPrice }} nF</div>
          </div>
        </div>
        <div class="w-50">
          <OrderConfirmButton
            :pulse="cartItems.length"
            :gray="isRestaurantClosed"
            :disabled="!cartItems.length || isRestaurantClosed"
            @click="confirm"
          >
            {{ $t('confirm_order') }}
          </OrderConfirmButton>
        </div>
      </div>

      <div class="container">
        <transition-group
          tag="div"
          name="list-complete"
          class="row"
        >
          <OrderSummaryItem
            v-for="item in cartItems"
            :key="item.increment"
            class="col-3 list-complete-item p-0"
          />
        </transition-group>
      </div>
    </div>

    <WarningClosed v-if="isRestaurantClosed"/>
  </div>
</template>

<script>
import OrderSummaryItem from '@/components/OrderSummaryItem.vue'
import OrderConfirmButton from '@/components/OrderConfirmButton.vue'
import WarningClosed from '@/components/WarningClosed.vue'
import OrderNotification from '@/components/OrderNotification.vue'
import orderStore from '@/store/orderStore.js'
import progressionStore from '@/store/progressionStore.js'

export default {
  name: "OrderSummary",
  components: {
    OrderSummaryItem,
    OrderConfirmButton,
    WarningClosed,
    OrderNotification,
  },
  data() {
    return {
      autocloseNotification: null,
    }
  },
  computed: {
    isCartFull: function() {
      return orderStore.getters.isCartFull
    },
    cartItems: function() {
      return orderStore.state.cartItems
    },
    totalPrice: function() {
      return orderStore.getters.totalPrice
    },
    isRestaurantClosed: function() {
      return progressionStore.state.isRestaurantClosed
    },
    displayOrderNotification: function() {
      return orderStore.state.displayOrderNotification
    },
  },
  methods: {
    reset: function() {
      orderStore.commit('resetOrder')
    },
    confirm: function() {
      this.autocloseNotification = setTimeout(this.acknowledgeNotification, 15000)
      orderStore.commit('confirmOrder')
    },
    acknowledgeNotification() {
      clearTimeout(this.autocloseNotification)
      orderStore.commit('acknowledgeOrderNotification')
    },
  }
}
</script>

<style scoped>
.list-complete {
  transition: all 1s;
}

.list-complete-item {
  transition: all 1s;
}

.list-complete-enter {
  transform: translateX(-100%);
}

.list-complete-leave-to {
  opacity: 0;
  transform: translateY(500px);
}

.list-complete-leave-active {
  position: absolute;
}

.very-small {
  font-size: 0.7rem;
}
</style>
