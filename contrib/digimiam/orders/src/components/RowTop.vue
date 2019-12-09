<template>
  <div class="row flex-grow-1">
    <div class="col">
      <div class="container-fluid h-100 d-flex flex-column">
        <div class="row rounded bg-dark shadow-box-dark text-white">
          <NeonsPrimary class="ml-2"/>
          <div class="mx-3">
            <h3 class="size-12 py-1 mb-0">PLATS</h3>
          </div>
          <NeonsPrimary class="mr-2"/>
        </div>
        <div class="row flex-grow-1">
          <div class="col-4">
            <OrderableItem itemId="salade_flamande"/>
          </div>
          <div class="col-4">
            <OrderableItem itemId="cambraisienne"/>
          </div>
          <div class="col-4">
            <OrderableItem itemId="potjevleesch"/>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import NeonsPrimary from '@/components/NeonsPrimary.vue'
import OrderableItem from '@/components/OrderableItem.vue'

export default {
  name: "RowTop",
  components: {
    NeonsPrimary,
    OrderableItem,
  },
}
</script>
