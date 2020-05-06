<template>
  <g>
    <polygon
      v-for="v in vertices" :key="v.id"
      :fill="'rgb(' + v.color.r + ', ' + v.color.g + ', ' + v.color.b + ')'"
      :transform="'rotate(' + v.rotation + ' ' + v.x + ' ' + v.y + ')'"
      :points="getHexagonVertices(v)"
      :filter="'url(#' + v.glowing + ')'"
    />
  </g>
</template>

<script>
import lightStore from '@/store/lightStore.js'

export default {
  name: 'LightContainerVertices',
  data: function () {
    return {
      verticeDiameter: 32,
    }
  },
  computed: {
    getHexagonVertices: function() {
      return function(vertice) {
        var centerX = vertice.x
        var centerY = vertice.y

        var leftX = centerX - this.verticeDiameter / 2
        var leftY = centerY

        var topLeftX = centerX - this.verticeDiameter / 4
        var topLeftY = centerY - Math.sqrt(3 * this.verticeDiameter * this.verticeDiameter / 16)

        var topRightX = centerX + this.verticeDiameter / 4
        var topRightY = centerY - Math.sqrt(3 * this.verticeDiameter * this.verticeDiameter / 16)

        var rightX = centerX + this.verticeDiameter / 2
        var rightY = centerY

        var bottomRightX = centerX + this.verticeDiameter / 4
        var bottomRightY = centerY + Math.sqrt(3 * this.verticeDiameter * this.verticeDiameter / 16)

        var bottomLeftX = centerX - this.verticeDiameter / 4
        var bottomLeftY = centerY + Math.sqrt(3 * this.verticeDiameter * this.verticeDiameter / 16)

        return leftX + ',' + leftY + ' ' + topLeftX + ',' + topLeftY + ' ' + topRightX + ',' + topRightY + ' ' + rightX + ',' + rightY + ' ' + bottomRightX + ',' + bottomRightY + ' ' + bottomLeftX + ',' + bottomLeftY
      }
    },
    vertices: function() {
      return lightStore.state.vertices
    },
  },
}
</script>