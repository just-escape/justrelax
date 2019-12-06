<template>
  <div class="row flex-grow-1">
    <div class="col">
      <div class="container-fluid d-flex flex-column h-100">
        <div class="row rounded bg-primary shadow-box-primary text-white">
          <div class="col">
            <h3 class="orderable-category py-1 mb-0">BOISSONS</h3>
          </div>
        </div>
        <div class="row flex-grow-1">
          <div class="col-4 flex-grow-1">
            <OrderableItem itemId="boisson1"/>
          </div>
          <div class="col-4 flex-grow-1">
            <OrderableItem itemId="boisson2"/>
          </div>
          <div class="col-4 flex-grow-1">
            <OrderableItem itemId="boisson3"/>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import OrderableItem from '@/components/OrderableItem.vue'

export default {
  name: "RowBottom",
  components: {
    OrderableItem
  },
}
</script>
