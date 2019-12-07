<template>
  <div class="row flex-grow-1">
    <div class="col-8">
      <div class="container-fluid h-100 d-flex flex-column">
        <div class="row rounded bg-dark shadow-box-dark text-white">
          <Neons class="ml-2"/>
          <div class="mx-3">
            <h3 class="orderable-category py-1 mb-0">SUPPLÉMENTS</h3>
          </div>
          <Neons class="mr-2"/>
        </div>
        <div class="row flex-grow-1">
          <div class="col-6 flex-grow-1">
            <OrderableItem itemId="frites"/>
          </div>
          <div class="col-6 flex-grow-1">
            <OrderableItem itemId="moules"/>
          </div>
        </div>
      </div>
    </div>
    <div class="col-4">
      <div class="container-fluid h-100 d-flex flex-column">
        <div class="row rounded bg-dark shadow-box-dark text-white">
          <Neons class="ml-2"/>
          <div class="mx-3">
            <h3 class="orderable-category py-1 mb-0">SAUCES</h3>
          </div>
          <Neons class="mr-2"/>
        </div>
        <div class="row flex-grow-1">
          <div class="col flex-grow-1">
            <SmallOrderableItem itemId="sauce1"/>
          </div>
        </div>
        <div class="row flex-grow-1">
          <div class="col flex-grow-1">
            <SmallOrderableItem itemId="sauce2"/>
          </div>
        </div>
        <div class="row flex-grow-1">
          <div class="col flex-grow-1">
            <SmallOrderableItem itemId="sauce3"/>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import Neons from '@/components/Neons.vue'
import OrderableItem from '@/components/OrderableItem.vue'
import SmallOrderableItem from '@/components/SmallOrderableItem.vue'

export default {
  name: "RowMiddle",
  components: {
    Neons,
    OrderableItem,
    SmallOrderableItem,
  },
}
</script>
