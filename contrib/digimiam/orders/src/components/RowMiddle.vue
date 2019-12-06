<template>
  <div class="row flex-grow-1">
    <div class="col-8">
      <div class="container-fluid h-100 d-flex flex-column">
        <div class="row rounded bg-primary shadow-box-primary text-white">
          <div class="col">
            <h3 class="orderable-category py-1 mb-0">SUPPLÉMENTS</h3>
          </div>
        </div>
        <div class="row flex-grow-1">
          <div class="col-6 flex-grow-1">
            <OrderableItem itemId="frites"/>
          </div>
          <div class="col-6 flex-grow-1">
            <OrderableItem itemId="maroilles"/>
          </div>
        </div>
      </div>
    </div>
    <div class="col-4">
      <div class="container-fluid h-100 d-flex flex-column">
        <div class="row rounded bg-primary shadow-box-primary text-white">
          <div class="col">
            <h3 class="orderable-category py-1 mb-0">DESSERT</h3>
          </div>
        </div>
        <div class="row flex-grow-1">
          <div class="col flex-grow-1">
            <OrderableItem itemId="gaufresque"/>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import OrderableItem from '@/components/OrderableItem.vue'

export default {
  name: "RowMiddle",
  components: {
    OrderableItem
  },
}
</script>
