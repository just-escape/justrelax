<template>
  <g>
    <path
      :d="getPathVertices(centerX, centerY, diameter)"
      :stroke="'rgba(0, 209, 182, ' + opacity + ')'"
      :fill="getFill"
      :stroke-width="strokeWidth"
    />
  </g>
</template>

<script>
export default {
  name: 'LightContainerGeneratorHexagon',
  computed: {
    getCoordinates: function() {
      return function(centerX, centerY, diameter) {
        let leftX = centerX - diameter / 2
        let leftY = centerY

        let topLeftX = centerX - diameter / 4
        let topLeftY = centerY - Math.sqrt(3 * diameter * diameter / 16)

        let topRightX = centerX + diameter / 4
        let topRightY = centerY - Math.sqrt(3 * diameter * diameter / 16)

        let rightX = centerX + diameter / 2
        let rightY = centerY

        let bottomRightX = centerX + diameter / 4
        let bottomRightY = centerY + Math.sqrt(3 * diameter * diameter / 16)

        let bottomLeftX = centerX - diameter / 4
        let bottomLeftY = centerY + Math.sqrt(3 * diameter * diameter / 16)

        return [
          {x: leftX, y: leftY},
          {x: topLeftX, y: topLeftY},
          {x: topRightX, y: topRightY},
          {x: rightX, y: rightY},
          {x: bottomRightX, y: bottomRightY},
          {x: bottomLeftX, y: bottomLeftY},
        ]
      }
    },
    getPathVertices: function() {
      return function(centerX, centerY, diameter) {
        let c = this.getCoordinates(centerX, centerY, diameter)
        return 'M ' +
          c[0].x + ' ' + c[0].y + ' L ' +
          c[1].x + ' ' + c[1].y + ' L ' +
          c[2].x + ' ' + c[2].y + ' L ' +
          c[3].x + ' ' + c[3].y + ' L ' +
          c[4].x + ' ' + c[4].y + ' L ' +
          c[5].x + ' ' + c[5].y + ' Z'
      }
    },
    getFill: function() {
      if (this.filled) {
        return 'rgba(0, 209, 182, ' + this.opacity + ')'
      } else {
        return "rgba(0, 0, 0, 0)"
      }
    },
  },
  props: {
    centerX: {
      type: Number,
      required: true,
    },
    centerY: {
      type: Number,
      required: true,
    },
    diameter: {
      type: Number,
      required: true,
    },
    opacity: {
      type: Number,
      required: false,
      default: 1,
    },
    strokeWidth: {
      type: Number,
      required: false,
      default: 0,
    },
    filled: {
      type: Boolean,
      required: false,
      default: false,
    },
  }
}
</script>