<template>
  <div class="d-flex flex-column flex-grow-1 rounded overflow-hidden p-4">

    <div class="d-flex flex-row justify-content-end align-items-end mb-2 px-2">
      <div class="text-orange text-right pr-3">
        <div class="font-weight-bold">Cart is full</div>
        <div class="small">Confirm or reset your order</div>
      </div>
      <div class="w-50">
        <b-btn block variant="outline-info py-2" @click="trashbin">RESET ORDER</b-btn>
      </div>
    </div>

    <div class="d-flex flex-row justify-content-end align-items-center mb-4 px-2">
      <div class="text-white pr-3">
        <div class="d-flex flex-row font-weight-bold">
          <div>Total: {{ totalPrice }} nF</div>
        </div>
      </div>
      <div class="w-50">
        <OrderConfirmButton :pulse="true">CONFIRM ORDER</OrderConfirmButton>
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
</template>

<script>
import OrderSummaryItem from '@/components/OrderSummaryItem.vue'
import OrderConfirmButton from '@/components/OrderConfirmButton.vue'
import orderStore from '@/store/orderStore.js'

export default {
  name: "OrderSummary",
  components: {
    OrderSummaryItem,
    OrderConfirmButton,
  },
  computed: {
    cartItems: function() {
      return orderStore.state.cartItems
    },
    totalPrice: function() {
      var price = 0
      return price
    },
  },
  methods: {
    trashbin: function() {
      orderStore.commit('resetOrder')
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
