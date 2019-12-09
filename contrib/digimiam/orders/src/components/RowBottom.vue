<template>
  <div class="row flex-grow-1">
    <div class="col-8">
      <div class="container-fluid d-flex flex-column h-100">
        <div class="row rounded bg-dark shadow-box-dark text-white">
          <NeonsPrimary class="ml-2"/>
          <div class="mx-3">
            <h3 class="size-12 py-1 mb-0">BOISSONS</h3>
          </div>
          <NeonsPrimary class="mr-2"/>
        </div>
        <div class="row flex-grow-1">
          <div class="col-6 flex-grow-1">
            <OrderableItem itemId="boisson1"/>
          </div>
          <div class="col-6 flex-grow-1">
            <OrderableItem itemId="boisson2"/>
          </div>
        </div>
      </div>
    </div>
    <div class="col-4">
      <div class="container-fluid h-100 d-flex flex-column">
        <div class="row rounded bg-dark shadow-box-dark text-white">
          <NeonsPrimary class="ml-2"/>
          <div class="mx-3">
            <h3 class="size-12 py-1 mb-0">DESSERT</h3>
          </div>
          <NeonsPrimary class="mr-2"/>
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
import NeonsPrimary from '@/components/NeonsPrimary.vue'
import OrderableItem from '@/components/OrderableItem.vue'

export default {
  name: "RowBottom",
  components: {
    NeonsPrimary,
    OrderableItem,
  },
}
</script>
