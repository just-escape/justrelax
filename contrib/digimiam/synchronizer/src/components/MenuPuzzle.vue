<template>
  <div class="position-relative">
    <div class="container-fluid px-0 h-100">
      <div class="row justify-content-center h-100">
        <div class="w-large">
          <DishMatrix/>
        </div>

        <div class="w-small">
          <MenuDisplay/>
        </div>

        <div class="glowing-wire top-wire"></div>
        <div class="glowing-wire bottom-wire"></div>
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

<style scoped>
.glowing-wire {
  position: absolute;
  width: calc(2 * 15px + 16px);
  height: 1px;
  left: 830px;
  border-top: 1px solid #00d1b6;
  box-shadow: 0px 1px 3px 0.01px rgba(0, 209, 182, 0.7);
}

.top-wire {
  top: 30%;
}

.bottom-wire {
  bottom: 30%;
}
</style>