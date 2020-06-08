<template>
  <div class="glowing-container h-100 w-100 position-absolute" :style="{transform: transform}">
    <div class="d-flex flex-column h-100">
      <div v-for="(row, rowIndex) in map" :key="rowIndex" class="d-flex flex-row flex-grow-1">
        <Cell v-for="(cellContent, cellIndex) in row" :key="cellIndex" class="flex-grow-1" :content="cellContent"/>
      </div>
    </div>
  </div>
</template>

<script>
import Cell from '@/components/Cell.vue'

export default {
  name: "Level",
  components: {
    Cell,
  },
  props: {
    transform: String,
    map: Array,
  },
}
</script>