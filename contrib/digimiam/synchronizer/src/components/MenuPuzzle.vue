<template>
  <div class="position-relative">
    <div class="container-fluid px-0 h-100">
      <div class="row h-100">
        <div class="col-8">
          <MealSelector/>
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
import MealSelector from '@/components/MealSelector.vue'

export default {
  name: 'MenuSelector',
  components: {
    MenuDisplay,
    MealSelector,
  },
}
</script>

<style scoped>
.meal-name-label {
  background: #006107;
  border-radius: 1px;
  padding: 1px 4px;
}
</style>
