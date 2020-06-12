<template>
  <div class="glowing-container h-100 w-100 position-absolute" :style="{transform: transform}">
    <div class="d-flex flex-column h-100">
      <div v-for="(row, rowIndex) in map" :key="rowIndex" class="d-flex flex-row flex-grow-1">
        <Cell v-for="(cellContent, cellIndex) in row" :key="cellIndex" class="flex-grow-1" :content="cellContent"/>
      </div>
    </div>

    <Cell
      v-for="(block, blockIndex) in blocks" :key="blockIndex"
      class="position-absolute" :style="{height: height, width: width, top: getTop(block.y), left: getLeft(block.x)}" content="B"
    />
  </div>
</template>

<script>
import Cell from '@/components/Cell.vue'
import sokobanStore from '@/store/sokobanStore.js'

export default {
  name: "Level",
  components: {
    Cell,
  },
  computed: {
    width() {
      return this.sceneSize / sokobanStore.state.cols + 'px'
    },
    height() {
      return this.sceneSize / sokobanStore.state.rows + 'px'
    },
    getTop() {
      return function (y) {
        return (y * this.sceneSize / sokobanStore.state.cols - 1) + 'px'
      }
    },
    getLeft() {
      return function (x) {
        return (x * this.sceneSize / sokobanStore.state.rows - 1) + 'px'
      }
    },
  },
  props: {
    transform: String,
    map: Array,
    blocks: Array,
    sceneSize: Number,
  },
}
</script>