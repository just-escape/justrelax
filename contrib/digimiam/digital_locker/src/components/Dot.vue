<template>
  <div class="position-absolute" :style="{top: top + 'px', left: left + 'px'}">
    <div class="position-relative">
      <SvgHexagon class="hexagon"/>
      <div
        @mousemove="connect" @touchmove="connect"
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
import lockerStore from '@/store/lockerStore.js'

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
      return 'border-color ' + lockerStore.state.connectorsColorTransition + 's ease-out, background ' + lockerStore.state.connectorsColorTransition + 's ease-out'
    },
    circleBorderColor() {
      return 'rgba(' + lockerStore.state.connectorsColor.r + ', ' + lockerStore.state.connectorsColor.g + ', ' + lockerStore.state.connectorsColor.b + ', 0.7)'
    },
    circleBackground() {
      return 'rgba(' + lockerStore.state.connectorsColor.r + ', ' + lockerStore.state.connectorsColor.g + ', ' + lockerStore.state.connectorsColor.b + ', 0.18)'
    },
  },
  methods: {
    connect() {
      lockerStore.commit('connect', this.index)

      lockerStore.commit('checkPattern')
      if (lockerStore.state.success) {
        lockerStore.commit('setConnectorsColorTransition', 0.8)
        lockerStore.commit('showSuccess')
        setTimeout(lockerStore.commit, 801, 'setConnectorsColorTransition', 0)
        setTimeout(lockerStore.commit, 1200, 'resetPattern')
        setTimeout(lockerStore.commit, 1200, 'notifySuccess')
      }
    },
    startPattern() {
      lockerStore.commit('startPattern', this.index)
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