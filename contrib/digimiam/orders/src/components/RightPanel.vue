<template>
  <div class="d-flex flex-column justify-content-between h-100">
    <div class="d-flex flex-column flex-grow-1">
      <div class="mb-3">
        <Marmitron/>
      </div>
      <div class="flex-grow-1 mb-4">
        <OrderSummary/>
      </div>
    </div>
    <RightPanelButtons/>
  </div>
</template>

<script>
import Marmitron from '@/components/Marmitron.vue'
import OrderSummary from '@/components/OrderSummary.vue'
import RightPanelButtons from '@/components/RightPanelButtons.vue'

export default {
  name: "RightPanel",
  components: {
    Marmitron,
    OrderSummary,
    RightPanelButtons,
  },
}
</script>
