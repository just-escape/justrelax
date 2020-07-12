<template>
  <div class="position-absolute" :style="{top: top + 'px', left: left + 'px'}">
    <div class="position-relative">
      <SvgHexagon class="hexagon"/>
      <div
        @mousedown="startPattern" @touchstart="startPattern"
        class="circle"
        :style="{
          opacity: circleOpacity,
          'border-color': circleBorderColor,
          background: circleBackground,
          transition: circleTransition,
        }"
      ></div>
    </div>
  </div>
</template>

<script>
import SvgHexagon from '@/components/SvgHexagon.vue'
import lockStore from '@/store/lockStore.js'

export default {
  name: "Dot",
  components: {
    SvgHexagon
  },
  computed: {
    circleOpacity() {
      if (this.connected) {
        return 1
      } else {
        return 0
      }
    },
    circleTransition() {
      return 'border-color ' + lockStore.state.connectorsColorTransition + 's ease-out, background ' + lockStore.state.connectorsColorTransition + 's ease-out'
    },
    circleBorderColor() {
      return 'rgba(' + lockStore.state.connectorsColor.r + ', ' + lockStore.state.connectorsColor.g + ', ' + lockStore.state.connectorsColor.b + ', 0.7)'
    },
    circleBackground() {
      return 'rgba(' + lockStore.state.connectorsColor.r + ', ' + lockStore.state.connectorsColor.g + ', ' + lockStore.state.connectorsColor.b + ', 0.18)'
    },
  },
  methods: {
    startPattern() {
      lockStore.commit('startPattern', this.index)
    },
  },
  props: {
    top: Number,
    left: Number,
    connected: Boolean,
    index: Number,
  },
}
</script>

<style scoped>
.hexagon {
  width: 50px;
  position: absolute;
  top: -25px;
  left: -25px;
}

.circle {
  position: absolute;
  top: -35px;
  left: -35px;
  width: 70px;
  height: 70px;
  border-radius: 50%;
  border-width: 4px;
  border-style: solid;
}
</style>