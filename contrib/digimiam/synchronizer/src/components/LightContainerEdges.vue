<template>
  <g>
    <polygon
      v-for="(e, eId) in horizontalEdges" :key="e.id"
      :fill="getEdgeColor(e, eId)"
      :points="getHorizontalEdgePoints(e)"
      :filter="getEdgeGlow(e)"
    />
    <path
      v-for="(e, eId) in diagonalEdges" :key="e.id"
      :stroke="getEdgeColor(e, eId)"
      :d="getDiagonalEdgePoints(e)"
      :filter="getEdgeGlow(e)"
      stroke-width="8"
    />
  </g>
</template>

<script>
import lightStore from '@/store/lightStore.js'

export default {
  name: 'LightContainerEdges',
  computed: {
    horizontalEdges: function() {
      var horizontalEdges = {}
      for (var eId in lightStore.state.edges) {
        var direction = lightStore.state.edges[eId].getDirection()
        if (direction == 'left-right' || direction == 'right-left') {
          horizontalEdges[eId] = lightStore.state.edges[eId]
        }
      }
      return horizontalEdges
    },
    diagonalEdges: function() {
      var diagonalEdges = {}
      for (var eId in lightStore.state.edges) {
        var direction = lightStore.state.edges[eId].getDirection()
        if (!(direction == 'left-right' || direction == 'right-left')) {
          diagonalEdges[eId] = lightStore.state.edges[eId]
        }
      }
      return diagonalEdges
    },
    getHorizontalEdgePoints: function() {
      return function(edge) {
        var offset = 4

        var topLeftX = lightStore.state.vertices[edge.getVertice1()].x
        var topLeftY = lightStore.state.vertices[edge.getVertice1()].y - offset
        var topRightX = lightStore.state.vertices[edge.getVertice2()].x
        var topRightY = lightStore.state.vertices[edge.getVertice2()].y - offset
        var bottomRightX = lightStore.state.vertices[edge.getVertice2()].x
        var bottomRightY = lightStore.state.vertices[edge.getVertice2()].y + offset
        var bottomLeftX = lightStore.state.vertices[edge.getVertice1()].x
        var bottomLeftY = lightStore.state.vertices[edge.getVertice1()].y + offset

        return topLeftX + ',' + topLeftY + ' ' + topRightX + ',' + topRightY + ' ' + bottomRightX + ',' + bottomRightY + ' ' + bottomLeftX + ',' + bottomLeftY
      }
    },
    getDiagonalEdgePoints: function() {
      return function(edge) {
        var x1 = lightStore.state.vertices[edge.getVertice1()].x
        var y1 = lightStore.state.vertices[edge.getVertice1()].y
        var x2 = lightStore.state.vertices[edge.getVertice2()].x
        var y2 = lightStore.state.vertices[edge.getVertice2()].y

        return 'M' + x1 + ' ' + y1 + ' L ' + x2 + ' ' + y2
      }
    },
    getEdgeColor: function() {
      return function(edge) {
        if (edge.validated) {
          return lightStore.state.colorValidated
        }

        if (edge.activated) {
          return 'url(#activation-' + edge.getDirection() + ')'
        }

        if (edge.activationPathAnimation) {
          return 'url(#activation-path-animation-' + edge.getDirection() + ')'
        }

        if (edge.finalAnimation) {
          return 'url(#final-animation-' + edge.getDirection() + ')'
        }

        return edge.color
      }
    },
    getEdgeGlow: function() {
      return function(edge) {
        if (edge.activated || edge.finalAnimation) {
          return 'url(#glowing-more)'
        } else {
          return ''
        }
      }
    },
  },
}
</script>