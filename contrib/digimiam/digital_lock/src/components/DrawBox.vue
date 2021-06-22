<template>
  <div
    ref="drawBox"
    class="position-relative"
  >
    <div class="box position-relative">
      <div class="position-absolute d-flex flex-column justify-content-between h-100 w-100" style="top: 0; left: 0">
        <div
          v-for="index in 13" :key="index"
          style="height: 30px; width: 100%; background: linear-gradient(to bottom, rgba(0, 209, 182, 0) 0%, rgba(0, 209, 182, 0.4) 70%, rgba(0, 209, 182, 0.4) 80%, rgba(0, 209, 182, 0) 100%)"
        />
      </div>
      <div class="position-absolute d-flex flex-row justify-content-between h-100 w-100" style="top: 0; left: 0">
        <div
          v-for="index in 13" :key="index"
          style="height: 100%; width: 30px; background: linear-gradient(to right, rgba(0, 209, 182, 0) 0%, rgba(0, 209, 182, 0.4) 70%, rgba(0, 209, 182, 0.4) 80%, rgba(0, 209, 182, 0) 100%)"
        />
      </div>
      <Dot
        v-for="(dot, dotIndex) in dots"
        :key="dotIndex"
        :left="dot.x"
        :top="dot.y"
        :connected="dot.connected"
        :index="dotIndex"
      />
    <div>
      <PatternLine
        v-for="(l, lIndex) in lines"
        :key="lIndex"
        :x1="l.x1"
        :y1="l.y1"
        :x2="l.x2"
        :y2="l.y2"
      />
    </div>
    </div>
  </div>
</template>

<script>
import PatternLine from '@/components/PatternLine.vue'
import Dot from '@/components/Dot.vue'
import lockStore from '@/store/lockStore.js'

export default {
  name: "DrawBox",
  components: {
    PatternLine,
    Dot,
  },
  computed: {
    dots() {
      return lockStore.state.dots
    },
    lines() {
      var lines = []

      for (var connection of lockStore.state.connections) {
        var dot1 = lockStore.state.dots[connection[0]]
        var dot2 = lockStore.state.dots[connection[1]]
        lines.push({
          x1: dot1.x,
          y1: dot1.y,
          x2: dot2.x,
          y2: dot2.y,
        })
      }

      if (lockStore.state.drawing) {
        lines.push({
          x1: lockStore.state.dots[lockStore.state.lastConnectedDotIndex].x,
          y1: lockStore.state.dots[lockStore.state.lastConnectedDotIndex].y,
          x2: lockStore.state.cursorPosition.x,
          y2: lockStore.state.cursorPosition.y,
        })
      }

      return lines
    },
  },
  mounted() {
    let box = this.$refs.drawBox
    lockStore.commit('setBoxOffset', {left: box.offsetLeft, top: box.offsetTop})
  },
}
</script>

<style scoped>
.box {
  width: 550px;
  height: 550px;
  border: 2.8px #00d1b6 solid;
  border-radius: 50%;
  box-shadow: 0px 0px 20px -6px rgba(0, 209, 182, 1);
  display: block; /* Removes a mysterious margin bottom */
  overflow: hidden;
}
</style>