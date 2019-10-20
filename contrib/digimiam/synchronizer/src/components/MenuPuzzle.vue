<template>
  <div class="position-relative">
    <div class="container-fluid px-0 h-100">
      <div class="row h-100">
        <div class="col-8">
          <DishMatrix/>
        </div>

        <div class="col-4">
          <MenuDisplay/>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import MenuDisplay from '@/components/MenuDisplay.vue'
import DishMatrix from '@/components/DishMatrix.vue'

export default {
  name: 'MenuSelector',
  components: {
    MenuDisplay,
    DishMatrix,
  },
}
</script>
