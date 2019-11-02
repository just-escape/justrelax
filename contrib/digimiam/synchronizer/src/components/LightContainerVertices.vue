<template>
  <g>
    <polygon
      v-for="v in vertices" :key="v.id"
      :fill="'rgb(' + v.color.r + ', ' + v.color.g + ', ' + v.color.b + ')'"
      :transform="'rotate(' + v.rotation + ' ' + v.x + ' ' + v.y + ')'"
      :points="getVerticeHexagon(v)"
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
    getVerticeHexagon: function() {
      return function(vertice) {
        var centerX = vertice.x
        var centerY = vertice.y

        var leftX = centerX - this.verticeDiameter / 2
        var leftY = centerY

        var topLeftX = centerX - this.verticeDiameter / 4
        // I don't know why + 1
        var topLeftY = centerY - this.verticeDiameter / 2 + 1

        var topRightX = centerX + this.verticeDiameter / 4
        // I don't know why + 1
        var topRightY = centerY - this.verticeDiameter / 2 + 1

        var rightX = centerX + this.verticeDiameter / 2
        var rightY = centerY

        var bottomRightX = centerX + this.verticeDiameter / 4
        // I don't know why - 1
        var bottomRightY = centerY + this.verticeDiameter / 2 - 1

        var bottomLeftX = centerX - this.verticeDiameter / 4
        // I don't know why - 1
        var bottomLeftY = centerY + this.verticeDiameter / 2 - 1

        return leftX + ',' + leftY + ' ' + topLeftX + ',' + topLeftY + ' ' + topRightX + ',' + topRightY + ' ' + rightX + ',' + rightY + ' ' + bottomRightX + ',' + bottomRightY + ' ' + bottomLeftX + ',' + bottomLeftY
      }
    },
    vertices: function() {
      return lightStore.state.vertices
    },
  },
}
</script>