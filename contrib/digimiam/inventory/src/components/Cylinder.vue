<template>
  <div class="d-flex justify-content-center align-items-center transition-400ms">
    <img src="@/assets/img/cylinder.png" class="img-fluid transition-opacity-200ms" :style="{opacity: opacity}"/>
  </div>
</template>

<script>
import sokobanStore from '@/store/sokobanStore.js'

export default {
  name: "Cylinder",
  computed: {
    areCylindersMobile() {
      return !sokobanStore.state.faceAnimationFlags[this.face].includes("turnCylinders")
    },
    opacity() {
      return this.areCylindersMobile ? 1 : 0
    },
  },
  props: {
    face: String,
    x: Number,
    y: Number,
  }
}
</script>