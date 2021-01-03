<template>
  <div class="h-100 w-100 position-absolute" :style="{transform: transform}">
    <div class="d-flex flex-column h-100">
      <div v-for="(row, rowIndex) in map" :key="rowIndex" class="d-flex flex-row flex-grow-1">
        <Cell v-for="(cell, cellIndex) in row" :key="cellIndex" class="flex-grow-1" :cell="cell" :face="face"/>
      </div>
    </div>

    <Cylinder
      v-for="(block, blockIndex) in blocks" :key="blockIndex"
      class="position-absolute" :style="{width: width, height: height, top: getTop(block.y), left: getLeft(block.x)}"
      :face="face"
      :x="block.x"
      :y="block.y"
    />

    <Marmitron
      class="position-absolute transition-400ms"
      v-if="marmitron.exist"
      :sceneSize="sceneSize" :style="{width: width, height: height, top: getTop(marmitron.y), left: getLeft(marmitron.x)}"
    />
  </div>
</template>

<script>
import Cell from '@/components/Cell.vue'
import Cylinder from '@/components/Cylinder.vue'
import Marmitron from '@/components/Marmitron.vue'
import sokobanStore from '@/store/sokobanStore.js'

export default {
  name: "Level",
  components: {
    Cell,
    Cylinder,
    Marmitron,
  },
  computed: {
    map() {
      return sokobanStore.state.grids[sokobanStore.state.difficulty][this.face]
    },
    blocks() {
      return sokobanStore.state.currentBlocks[this.face]
    },
    marmitron() {
      return sokobanStore.state.currentMarmitronPositions[this.face]
    },
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
    sceneSize: Number,
    face: String,
  },
}
</script>