<template>
  <div
    ref="drawBox"
    class="position-relative"
  >
    <div class="box"></div>
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
    <div>
      <Dot
        v-for="(dot, dotIndex) in dots"
        :key="dotIndex"
        :left="dot.x"
        :top="dot.y"
        :connected="dot.connected"
        :index="dotIndex"
      />
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
  height: 635px;
  border: 1px #00d1b6 solid;
  box-shadow: 0px 0px 14px -6px rgba(0, 209, 182, 1);
  display: block; /* Removes a mysterious margin bottom */
}
</style>