<template>
  <div class="row flex-grow-1">
    <div class="col">
      <div class="container-fluid h-100 d-flex flex-column">
        <div class="row rounded bg-primary shadow-box-primary text-white">
          <div class="col">
            <h3 class="orderable-category py-1 mb-0">PLATS</h3>
          </div>
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
import OrderableItem from '@/components/OrderableItem.vue'

export default {
  name: "RowTop",
  components: {
    OrderableItem
  },
}
</script>
