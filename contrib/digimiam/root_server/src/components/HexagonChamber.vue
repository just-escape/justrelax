<template>
  <div
    class="position-absolute"
    :style="{
      top: top + 'px',
      right: right + 'px',
      width: width + 'px',
      transform: 'scale(' + scale + ')',
    }"
  >
    <svg :viewBox="'-3 -3 ' + (w + 4.5) + ' ' + (h + 4.5)" class="svg-glowing">
      <polygon
        :points="edges"
        :stroke="'rgba(0, 209, 182, 1)'"
        stroke-width="3"
        :fill="'rgba(0, 209, 182, ' + fillOpacity + ')'"
      />
    </svg>
    <div class="position-absolute w-100 h-100 top-left">
      <div class="d-flex justify-content-center align-items-center h-100">
        <div v-if="availabilityLoading" class="loading"></div>
      </div>
    </div>
  </div>
</template>
<script>
import businessStore from '@/store/businessStore.js'

export default {
  name: "HexagonChamber",
  data() {
    return {
      size: 20,
      scale: 1,
      fillOpacity: 0,
    }
  },
  computed: {
    availabilityLoading() {
      return businessStore.state.availabilityLoading
    },
    h() {
      return Math.sqrt(3) * this.size
    },
    w() {
      return 2 * this.size
    },
    edges() {
      var leftX = 0
      var leftY = this.h / 2

      var topLeftX = 0.25 * this.w
      var topLeftY = 0

      var topRightX = 0.75 * this.w
      var topRightY = 0

      var rightX = this.w
      var rightY = this.h / 2

      var bottomRightX = 0.75 * this.w
      var bottomRightY = this.h

      var bottomLeftX = 0.25 * this.w
      var bottomLeftY = this.h

      return leftX + ',' + leftY + ' ' + topLeftX + ',' + topLeftY + ' ' + topRightX + ',' + topRightY + ' ' + rightX + ',' + rightY + ' ' + bottomRightX + ',' + bottomRightY + ' ' + bottomLeftX + ',' + bottomLeftY
    },
  },
  props: {
    top: Number,
    right: Number,
    width: Number,
  },
}
</script>