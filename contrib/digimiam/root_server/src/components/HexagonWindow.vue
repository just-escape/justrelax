<template>
  <div class="position-absolute hexagon-window">
    <svg :viewBox="'0 0 ' + boxWidth + ' ' + boxHeight" class="h-100 w-100">
      <polygon :points="edges" stroke="red" stroke-width="1"/>
    </svg>
  </div>
</template>

<script>
export default {
  name: "HexagonWindow",
  data() {
    return {
      boxWidth: 250,
      boxHeight: 250,
      size: 40,
    }
  },
  computed: {
    h() {
      return Math.sqrt(3) * this.size
    },
    w() {
      return 2 * this.size
    },
    edges() {
      var centerX = this.boxWidth / 2
      var centerY = this.boxHeight / 2

      var leftX = centerX - this.w
      var leftY = centerY

      var topLeftX = centerX - this.w / 2
      var topLeftY = centerY - this.h

      var topRightX = centerX + this.w / 2
      var topRightY = centerY - this.h

      var rightX = centerX + this.w
      var rightY = centerY

      var bottomRightX = centerX + this.w / 2
      var bottomRightY = centerY + this.h

      var bottomLeftX = centerX - this.w / 2
      var bottomLeftY = centerY + this.h

      return leftX + ',' + leftY + ' ' + topLeftX + ',' + topLeftY + ' ' + topRightX + ',' + topRightY + ' ' + rightX + ',' + rightY + ' ' + bottomRightX + ',' + bottomRightY + ' ' + bottomLeftX + ',' + bottomLeftY
    },
  }
}
</script>

<style scoped>
.hexagon-window {
  height: 300px;
  width: 300px;
}
</style>