<template>
  <div
    class="position-absolute transition-1s d-flex justify-content-center align-items-center"
    :style="{width: width, height: height, top: top, left: left}"
    style="font-size: 100px"
  >
    M
  </div>
</template>

<script>
import sokobanStore from '@/store/sokobanStore.js'

export default {
  name: "Marmitron",
  computed: {
    width() {
      return this.sceneSize / sokobanStore.state.cols + 'px'
    },
    height() {
      return this.sceneSize / sokobanStore.state.rows + 'px'
    },
    top() {
      return sokobanStore.state.marmitronPosition.y * this.sceneSize / sokobanStore.state.cols + 'px'
    },
    left() {
      return sokobanStore.state.marmitronPosition.x * this.sceneSize / sokobanStore.state.rows + 'px'
    },
  },
  props: {
    sceneSize: Number,
  },
}
</script>