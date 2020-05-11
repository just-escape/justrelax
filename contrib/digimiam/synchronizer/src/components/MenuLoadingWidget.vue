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
          x: 137,
          y: 0,
          color: 'white',
          hidden: true,
          blinkAnimation: false,
        },
        {
          x: 157,
          y: 0,
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
        {
          x: 157,
          y: 34,
          color: 'white',
          hidden: true,
          blinkAnimation: false,
        },
        {
          x: 137,
          y: 34,
          color: 'white',
          hidden: true,
          blinkAnimation: false,
        },
        {
          x: 127,
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
      setTimeout(this.unlockAnimation, 4000)

      var color
      if (menuStore.getters.isSuccess) {
        color = "green"
      } else {
        color = "red"
      }

      for (var i = 0 ; i < this.hexagons.length ; i++) {
        setTimeout(this.startHexagonAnimation, 150 * i, i)
        setTimeout(this.showHexagon, 150 * i, i)

        setTimeout(this.stopHexagonAnimation, 3400, i)
        setTimeout(this.hideHexagon, 3400, i)

        setTimeout(this.setHexagonColor, 3450, i, color)

        setTimeout(this.showHexagon, 3500, i)
        setTimeout(this.hideHexagon, 3600, i)
        setTimeout(this.showHexagon, 3700, i)
        setTimeout(this.hideHexagon, 3800, i)

        setTimeout(this.setHexagonColor, 3850, i, 'white')
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
  width: 12px;
}
</style>