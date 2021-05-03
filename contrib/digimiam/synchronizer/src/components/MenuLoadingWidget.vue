<template>
  <div class="position-relative">
    <MenuLoadingWidgetHexagon
      v-for="(hexagon, hexagonIndex) in hexagons"
      :key="hexagonIndex"
      class="hexagon"
      :hidden="hexagon.hidden"
      :positionX="hexagon.x"
      :positionY="hexagon.y"
      :color="hexagon.color"
      :blinkAnimation="hexagon.blinkAnimation"
    />
  </div>
</template>

<script>
import MenuLoadingWidgetHexagon from '@/components/MenuLoadingWidgetHexagon.vue'
import menuStore from '@/store/menuStore.js'

export default {
  name: 'MenuLoadingWidget',
  components: {
    MenuLoadingWidgetHexagon,
  },
  data() {
    return {
      hexagons: [
        {
          x: 177,
          y: 0,
          color: 'white',
          hidden: true,
          blinkAnimation: false,
        },
        {
          x: 197,
          y: 0,
          color: 'white',
          hidden: true,
          blinkAnimation: false,
        },
        {
          x: 207,
          y: 17,
          color: 'white',
          hidden: true,
          blinkAnimation: false,
        },
        {
          x: 197,
          y: 34,
          color: 'white',
          hidden: true,
          blinkAnimation: false,
        },
        {
          x: 177,
          y: 34,
          color: 'white',
          hidden: true,
          blinkAnimation: false,
        },
        {
          x: 167,
          y: 17,
          color: 'white',
          hidden: true,
          blinkAnimation: false,
        },
      ],
      animationRunning: false,
    }
  },
  methods: {
    startHexagonAnimation (hexagonIndex) {
      this.hexagons[hexagonIndex].blinkAnimation = true
    },
    stopHexagonAnimation (hexagonIndex) {
      this.hexagons[hexagonIndex].blinkAnimation = false
    },
    hideHexagon (hexagonIndex) {
      this.hexagons[hexagonIndex].hidden = true
    },
    showHexagon (hexagonIndex) {
      this.hexagons[hexagonIndex].hidden = false
    },
    setHexagonColor (hexagonIndex, color) {
      this.hexagons[hexagonIndex].color = color
    },
    lockAnimation() {
      this.animationRunning = true
    },
    unlockAnimation() {
      this.animationRunning = false
    },
  },
  watch: {
    startAnimationSignal() {
      // Protection
      if (this.animationRunning) {
        return
      }
      this.lockAnimation()
      setTimeout(this.unlockAnimation, 1500)

      var color
      if (menuStore.getters.isSuccess) {
        color = "green"
      } else {
        color = "red"
      }

      for (var i = 0 ; i < this.hexagons.length ; i++) {
        setTimeout(this.startHexagonAnimation, 150 * i, i)
        setTimeout(this.showHexagon, 150 * i, i)

        setTimeout(this.stopHexagonAnimation, 900, i)
        setTimeout(this.hideHexagon, 900, i)

        setTimeout(this.setHexagonColor, 950, i, color)

        setTimeout(this.showHexagon, 1000, i)
        setTimeout(this.hideHexagon, 1100, i)
        setTimeout(this.showHexagon, 1200, i)
        setTimeout(this.hideHexagon, 1300, i)

        setTimeout(this.setHexagonColor, 1350, i, 'white')
      }
    }
  },
  props: {
    startAnimationSignal: Boolean,
  },
}
</script>

<style scoped>
.hexagon {
  width: 18px;
}
</style>