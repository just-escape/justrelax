<template>
  <g>
    <LightContainerGeneratorHexagon
      v-for="(bgh, bghIndex) in backgroundHexagons"
      :key="bghIndex"
      :centerX="bgh.x"
      :centerY="bgh.y"
      :diameter="backgroundHexagonsFillDiamater"
      :filled="true"
      :opacity="bgh.opacity"
    />
    <LightContainerGeneratorHexagon
      v-for="(fgh, fghIndex) in foregroundHexagons"
      :key="fghIndex"
      :centerX="fgh.x"
      :centerY="fgh.y"
      :diameter="fgh.diameter"
      :filled="false"
      :strokeWidth="fgh.strokeWidth"
      :opacity="fgh.opacity"
    />
  </g>
</template>

<script>
import LightContainerGeneratorHexagon from '@/components/LightContainerGeneratorHexagon.vue'

export default {
  name: 'LightContainerGenerator',
  components: {
    LightContainerGeneratorHexagon,
  },
  data() {
    return {
      backgroundHexagonsOffsetX: -37.5,
      backgroundHexagonsOffsetY: 23,
      backgroundHexagonsDiameter: 120,
      backgroundHexagonsFillDiamater: 110,
      foregroundHexagons: [
        {
          x: 100,
          y: 152,
          diameter: 50,
          strokeWidth: 0.5,
          opacity: 0.5,
        },
        {
          x: 60,
          y: 100,
          diameter: 100,
          strokeWidth: 0.5,
          opacity: 0.7,
        },
        {
          x: 125,
          y: 50,
          diameter: 65,
          strokeWidth: 0.5,
          opacity: 0.5,
        },
        {
          x: 65,
          y: 10,
          diameter: 85,
          strokeWidth: 0.5,
          opacity: 0.4,
        },
        {
          x: 130,
          y: 130,
          diameter: 95,
          strokeWidth: 0.5,
          opacity: 0.3,
        },
        {
          x: 135,
          y: 230,
          diameter: 70,
          strokeWidth: 0.5,
          opacity: 0.3,
        },
        {
          x: 0,
          y: 200,
          diameter: 95,
          strokeWidth: 0.5,
          opacity: 0.4,
        },
        {
          x: 140,
          y: 5,
          diameter: 85,
          strokeWidth: 0.5,
          opacity: 0.9,
        },
        {
          x: 30,
          y: 150,
          diameter: 45,
          strokeWidth: 0.5,
          opacity: 0.6,
        },
        {
          x: 10,
          y: 130,
          diameter: 25,
          strokeWidth: 0.5,
          opacity: 0.8,
        },
        {
          x: 125,
          y: 20,
          diameter: 90,
          strokeWidth: 2,
          opacity: 0.5,
        },
        {
          x: 25,
          y: 70,
          diameter: 65,
          strokeWidth: 2,
          opacity: 0.4,
        },
        {
          x: 95,
          y: 70,
          diameter: 75,
          strokeWidth: 2,
          opacity: 0.8,
        },
        {
          x: 65,
          y: 150,
          diameter: 95,
          strokeWidth: 2,
          opacity: 0.6,
        },
        {
          x: 45,
          y: 0,
          diameter: 70,
          strokeWidth: 2,
          opacity: 0.55,
        },
        {
          x: 147,
          y: 130,
          diameter: 65,
          strokeWidth: 2,
          opacity: 0.7,
        },
        {
          x: 110,
          y: 185,
          diameter: 65,
          strokeWidth: 2,
          opacity: 0.8,
        },
        {
          x: 20,
          y: 270,
          diameter: 50,
          strokeWidth: 2,
          opacity: 0.55,
        },
        {
          x: 150,
          y: 230,
          diameter: 50,
          strokeWidth: 2,
          opacity: 0.4,
        },
        {
          x: 30,
          y: 330,
          diameter: 50,
          strokeWidth: 2,
          opacity: 0.35,
        },
        {
          x: 140,
          y: 340,
          diameter: 80,
          strokeWidth: 2,
          opacity: 0.5,
        },
        {
          x: 70,
          y: 240,
          diameter: 55,
          strokeWidth: 2,
          opacity: 0.4,
        },
        {
          x: 110,
          y: 300,
          diameter: 35,
          strokeWidth: 2,
          opacity: 0.35,
        },
        {
          x: 95,
          y: 270,
          diameter: 75,
          strokeWidth: 2,
          opacity: 0.55,
        },
        {
          x: 80,
          y: 300,
          diameter: 120,
          strokeWidth: 0.5,
          opacity: 0.55,
        },
        {
          x: 77,
          y: 230,
          diameter: 70,
          strokeWidth: 0.5,
          opacity: 0.7,
        },
        {
          x: 80,
          y: 280,
          diameter: 50,
          strokeWidth: 0.5,
          opacity: 0.4,
        },
        {
          x: 100,
          y: 345,
          diameter: 70,
          strokeWidth: 0.5,
          opacity: 0.35,
        },
        {
          x: 150,
          y: 310,
          diameter: 25,
          strokeWidth: 0.5,
          opacity: 0.7,
        },
        {
          x: 150,
          y: 360,
          diameter: 65,
          strokeWidth: 0.5,
          opacity: 0.5,
        },
      ],
    }
  },
  computed: {
    backgroundHexagons: function() {
      return [
        {
          x: 3 / 4 * this.backgroundHexagonsDiameter + this.backgroundHexagonsOffsetX,
          y: -1 * Math.sqrt(3 * this.backgroundHexagonsDiameter * this.backgroundHexagonsDiameter / 16) + this.backgroundHexagonsOffsetY,
          opacity: 0.07,
        },
        {
          x: this.backgroundHexagonsOffsetX,
          y: this.backgroundHexagonsOffsetY,
          opacity: 0.06,
        },
        {
          x: this.backgroundHexagonsOffsetX,
          y: 2 * Math.sqrt(3 * this.backgroundHexagonsDiameter * this.backgroundHexagonsDiameter / 16) + this.backgroundHexagonsOffsetY,
          opacity: 0.1,
        },
        {
          x: 6 / 4 * this.backgroundHexagonsDiameter + this.backgroundHexagonsOffsetX,
          y: this.backgroundHexagonsOffsetY,
          opacity: 0.08,
        },
        {
          x: 3 / 4 * this.backgroundHexagonsDiameter + this.backgroundHexagonsOffsetX,
          y: Math.sqrt(3 * this.backgroundHexagonsDiameter * this.backgroundHexagonsDiameter / 16) + this.backgroundHexagonsOffsetY,
          opacity: 0.06,
        },
        {
          x: 3 / 4 * this.backgroundHexagonsDiameter + this.backgroundHexagonsOffsetX,
          y: 3 * Math.sqrt(3 * this.backgroundHexagonsDiameter * this.backgroundHexagonsDiameter / 16) + this.backgroundHexagonsOffsetY,
          opacity: 0.17,
        },
        {
          x: 6 / 4 * this.backgroundHexagonsDiameter + this.backgroundHexagonsOffsetX,
          y: 2 * Math.sqrt(3 * this.backgroundHexagonsDiameter * this.backgroundHexagonsDiameter / 16) + this.backgroundHexagonsOffsetY,
          opacity: 0.1,
        },
        {
          x: 6 / 4 * this.backgroundHexagonsDiameter + this.backgroundHexagonsOffsetX,
          y: 6 * Math.sqrt(3 * this.backgroundHexagonsDiameter * this.backgroundHexagonsDiameter / 16) + this.backgroundHexagonsOffsetY,
          opacity: 0.15,
        },
        {
          x: 6 / 4 * this.backgroundHexagonsDiameter + this.backgroundHexagonsOffsetX,
          y: 4 * Math.sqrt(3 * this.backgroundHexagonsDiameter * this.backgroundHexagonsDiameter / 16) + this.backgroundHexagonsOffsetY,
          opacity: 0.2,
        },
        {
          x: 3 / 4 * this.backgroundHexagonsDiameter + this.backgroundHexagonsOffsetX,
          y: 5 * Math.sqrt(3 * this.backgroundHexagonsDiameter * this.backgroundHexagonsDiameter / 16) + this.backgroundHexagonsOffsetY,
          opacity: 0.065,
        },
        {
          x: 3 / 4 * this.backgroundHexagonsDiameter + this.backgroundHexagonsOffsetX,
          y: 7 * Math.sqrt(3 * this.backgroundHexagonsDiameter * this.backgroundHexagonsDiameter / 16) + this.backgroundHexagonsOffsetY,
          opacity: 0.2,
        },
        {
          x: 0 / 4 * this.backgroundHexagonsDiameter + this.backgroundHexagonsOffsetX,
          y: 6 * Math.sqrt(3 * this.backgroundHexagonsDiameter * this.backgroundHexagonsDiameter / 16) + this.backgroundHexagonsOffsetY,
          opacity: 0.05,
        },
        {
          x: 0 / 4 * this.backgroundHexagonsDiameter + this.backgroundHexagonsOffsetX,
          y: 4 * Math.sqrt(3 * this.backgroundHexagonsDiameter * this.backgroundHexagonsDiameter / 16) + this.backgroundHexagonsOffsetY,
          opacity: 0.075,
        },
      ]
    },
  }
}
</script>