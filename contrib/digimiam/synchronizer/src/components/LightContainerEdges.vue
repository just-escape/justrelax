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
import LightStore2 from '@/store/LightStore2.js'

export default {
  name: 'LightContainerEdges',
  computed: {
    horizontalEdges: function() {
      var horizontalEdges = {}
      for (var eId in LightStore2.state.edges) {
        var direction = LightStore2.state.edges[eId].getDirection()
        if (direction == 'left-right' || direction == 'right-left') {
          horizontalEdges[eId] = LightStore2.state.edges[eId]
        }
      }
      return horizontalEdges
    },
    diagonalEdges: function() {
      var diagonalEdges = {}
      for (var eId in LightStore2.state.edges) {
        var direction = LightStore2.state.edges[eId].getDirection()
        if (!(direction == 'left-right' || direction == 'right-left')) {
          diagonalEdges[eId] = LightStore2.state.edges[eId]
        }
      }
      return diagonalEdges
    },
    getHorizontalEdgePoints: function() {
      return function(edge) {
        var offset = 4

        var topLeftX = LightStore2.state.vertices[edge.getVertice1()].x
        var topLeftY = LightStore2.state.vertices[edge.getVertice1()].y - offset
        var topRightX = LightStore2.state.vertices[edge.getVertice2()].x
        var topRightY = LightStore2.state.vertices[edge.getVertice2()].y - offset
        var bottomRightX = LightStore2.state.vertices[edge.getVertice2()].x
        var bottomRightY = LightStore2.state.vertices[edge.getVertice2()].y + offset
        var bottomLeftX = LightStore2.state.vertices[edge.getVertice1()].x
        var bottomLeftY = LightStore2.state.vertices[edge.getVertice1()].y + offset

        return topLeftX + ',' + topLeftY + ' ' + topRightX + ',' + topRightY + ' ' + bottomRightX + ',' + bottomRightY + ' ' + bottomLeftX + ',' + bottomLeftY
      }
    },
    getDiagonalEdgePoints: function() {
      return function(edge) {
        var x1 = LightStore2.state.vertices[edge.getVertice1()].x
        var y1 = LightStore2.state.vertices[edge.getVertice1()].y
        var x2 = LightStore2.state.vertices[edge.getVertice2()].x
        var y2 = LightStore2.state.vertices[edge.getVertice2()].y

        return 'M' + x1 + ' ' + y1 + ' L ' + x2 + ' ' + y2
      }
    },
    getEdgeColor: function() {
      return function(edge) {
        if (edge.validated) {
          return LightStore2.state.colorValidated
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