<template>
  <g>
    <polygon
      v-for="v in vertices" :key="v.id"
      :fill="getFill(v)"
      :stroke="getStroke(v)"
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
    getH: function() {
      return function(vertice) {
        var h = Math.sqrt(3 * this.verticeDiameter * this.verticeDiameter / 16)
        if (vertice.startingPoint) {
          h *= 0.87
        }
        return h
      }
    },
    getW: function() {
      return function(vertice) {
        var w = this.verticeDiameter / 2
        if (vertice.startingPoint) {
          w *= 0.87
        }
        return w
      }
    },
    getHexagonVertices: function() {
      return function(vertice) {
        var centerX = vertice.x
        var centerY = vertice.y

        var leftX = centerX - this.getW(vertice)
        var leftY = centerY

        var topLeftX = centerX - this.getW(vertice) / 2
        var topLeftY = centerY - this.getH(vertice)

        var topRightX = centerX + this.getW(vertice) / 2
        var topRightY = centerY - this.getH(vertice)

        var rightX = centerX + this.getW(vertice)
        var rightY = centerY

        var bottomRightX = centerX + this.getW(vertice) / 2
        var bottomRightY = centerY + this.getH(vertice)

        var bottomLeftX = centerX - this.getW(vertice) / 2
        var bottomLeftY = centerY + this.getH(vertice)

        return leftX + ',' + leftY + ' ' + topLeftX + ',' + topLeftY + ' ' + topRightX + ',' + topRightY + ' ' + rightX + ',' + rightY + ' ' + bottomRightX + ',' + bottomRightY + ' ' + bottomLeftX + ',' + bottomLeftY
      }
    },
    getFill: function() {
      return function(vertice) {
        if (vertice.startingPoint) {
          return 'rgba(0, 0, 0, 0)'
        } else {
          return 'rgba(' + vertice.color.r + ', ' + vertice.color.g + ', ' + vertice.color.b + ', ' + vertice.color.a + ')'
        }
      }
    },
    getStroke: function() {
      return function(vertice) {
        if (vertice.startingPoint) {
          return 'rgba(' + vertice.color.r + ', ' + vertice.color.g + ', ' + vertice.color.b + ', ' + vertice.color.a + ')'
        } else {
          return 'rgba(0, 0, 0, 0)'
        }
      }
    },
    vertices: function() {
      return lightStore.state.vertices
    },
  },
}
</script>

<style scoped>
polygon {
  stroke-width: 6px;
}
</style>