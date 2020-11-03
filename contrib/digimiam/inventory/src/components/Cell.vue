<template>
  <div class="position-relative transition-1s" :style="{'z-index': zIndex}">
    <img :src="texture" class="img-fluid"/>
    <img
      v-if="isChamber"
      class="position-absolute top-left img-fluid transition-1s"
      :src="foodTexture"
    />
    <span
      v-if="isChamber"
      class="position-absolute d-flex justify-content-end align-items-end w-100 h-100 p-id top-left transition-1s"
      style="font-size: 24px;"
      :style="{opacity: chamberIdOpacity}"
    >
      {{ cell.id }}
    </span>
  </div>
</template>

<script>
import sokobanStore from '@/store/sokobanStore.js'

export default {
  name: "Cell",
  computed: {
    areCylindersMobile() {
      return !sokobanStore.state.faceAnimationFlags[this.face].includes("turnCylinders")
    },
    isFoodDisplayed() {
      return sokobanStore.state.faceAnimationFlags[this.face].includes("displayFood")
    },
    areChamberIdsDisplayed() {
      return sokobanStore.state.faceAnimationFlags[this.face].includes("displayChamberIds")
    },
    areGatesActivated() {
      return sokobanStore.state.faceAnimationFlags[this.face].includes("activateGates")
    },
    isGate() {
      return ['gate-left', 'gate-right', 'gate-top', 'gate-bottom'].includes(this.cell.type)
    },
    isChamber() {
      return this.cell.type === 'chamber'
    },
    foodTexture() {
      return this.isFoodDisplayed ? this.cell.foodTexture : ""
    },
    chamberIdOpacity() {
      return this.areChamberIdsDisplayed ? 1 : 0
    },
    isGateActive() {
      if (this.cell.type === 'gate-right') {
        return this.areGatesActivated && sokobanStore.state.currentFace === 'left'
      } else if (this.cell.type === 'gate-left') {
        return sokobanStore.state.currentFace === 'front'
      } else if (this.cell.type === 'gate-top') {
        return this.areGatesActivated && sokobanStore.state.currentFace === 'front'
      } else if (this.cell.type === 'gate-bottom') {
        return sokobanStore.state.currentFace === 'top'
      } else {
        return false
      }
    },
    texture() {
      if (this.isGate) {
        return this.isGateActive ? this.cell.animatedTexture : this.cell.texture
      } else if (this.isChamber) {
        return this.areCylindersMobile ? this.cell.texture : this.cell.successTexture
      } else {
        return this.cell.texture
      }
    },
    currentLevel() {
      return sokobanStore.state.currentLevel
    },
    zIndex() {
      return this.isGate ? 10 : 0
    },
  },
  props: {
    cell: Object,
    face: String,
  }
}
</script>

<style>
.p-id {
  padding-right: 0.175rem;
  padding-bottom: 0.4rem;
}
</style>