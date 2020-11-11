<template>
  <div class="position-relative transition-1s">
    <img :src="texture" class="img-fluid z-index-10"/>

    <img
      v-if="isGate"
      class="position-absolute img-fluid top-left z-index-30"
      :src="gateTexture"
    />

    <img
      v-if="isChamber"
      class="position-absolute img-fluid top-left z-index-30"
      :style="{transform: foodTextureTransform}"
      :src="foodTexture"
    />
    <span
      v-if="isChamber"
      class="position-absolute d-flex justify-content-end align-items-end w-100 h-100 p-id top-left transition-1s z-index-40"
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
  data() {
    return {
      foodTextureStyle: {
        scaleX: 0,
        scaleY: 0,
      }
    }
  },
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
    foodTextureTransform() {
      return "scaleX(" + this.foodTextureStyle.scaleX + ") scaleY(" + this.foodTextureStyle.scaleY + ")"
    },
    foodTexture() {
      return this.isChamber ? this.cell.foodTexture : ""
    },
    chamberIdOpacity() {
      return this.areChamberIdsDisplayed ? 1 : 0
    },
    gateTexture() {
      if (this.cell.type === 'gate-right') {
        if (this.areGatesActivated && sokobanStore.state.currentFace === 'left') {
          return this.cell.animatedTextureFast
        }
      } else if (this.cell.type === 'gate-left') {
        if (sokobanStore.state.currentFace === 'front') {
          return this.cell.animatedTextureSlow
        }
      } else if (this.cell.type === 'gate-top') {
        if (this.areGatesActivated && sokobanStore.state.currentFace === 'front') {
          return this.cell.animatedTextureFast
        }
      } else if (this.cell.type === 'gate-bottom') {
        if (sokobanStore.state.currentFace === 'top') {
          return this.cell.animatedTextureSlow
        }
      }

      return this.cell.texture
    },
    texture() {
      if (this.isGate) {
        return this.cell.floorTexture
      } else if (this.isChamber) {
        return this.areCylindersMobile ? this.cell.texture : this.cell.successTexture
      } else {
        return this.cell.texture
      }
    },
    currentLevel() {
      return sokobanStore.state.currentLevel
    },
  },
  watch: {
    isFoodDisplayed() {
      this.$anime({
        targets: this.foodTextureStyle,
        scaleX: 1,
        scaleY: 1,
        duration: 1000,
        easing: 'easeInQuad'
      })
    }
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