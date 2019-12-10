<template>
  <div class="d-flex flex-column justify-content-between h-100">
    <div class="d-flex flex-column h-50">
      <OrderSummary class="mb-4"/>
      <RightPanelButtons/>
    </div>
    <div class="h-50">
      <Cart/>
    </div>
  </div>
</template>

<script>
import OrderSummary from '@/components/OrderSummary.vue'
import RightPanelButtons from '@/components/RightPanelButtons.vue'
import Cart from '@/components/Cart.vue'

export default {
  name: "RightPanel",
  components: {
    OrderSummary,
    RightPanelButtons,
    Cart,
  },
}
</script>
