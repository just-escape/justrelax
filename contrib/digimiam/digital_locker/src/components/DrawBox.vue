<template>
  <div
    id="draw-box"
    @mousemove="mousemove"
    @touchmove="touchmove"
    @mouseleave="leave"
    @touchleave="leave"
    @mouseup="release"
    @touchend="release"
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
import lockerStore from '@/store/lockerStore.js'

export default {
  name: "DrawBox",
  components: {
    PatternLine,
    Dot,
  },
  data() {
    return {
      boxOffsetTop: 0,
      boxOffsetLeft: 0,
    }
  },
  computed: {
    dots() {
      return lockerStore.state.dots
    },
    lines() {
      var lines = []

      for (var connection of lockerStore.state.connections) {
        var dot1 = lockerStore.state.dots[connection[0]]
        var dot2 = lockerStore.state.dots[connection[1]]
        lines.push({
          x1: dot1.x,
          y1: dot1.y,
          x2: dot2.x,
          y2: dot2.y,
        })
      }

      if (lockerStore.state.drawing) {
        lines.push({
          x1: lockerStore.state.dots[lockerStore.state.lastConnectedDotIndex].x,
          y1: lockerStore.state.dots[lockerStore.state.lastConnectedDotIndex].y,
          x2: lockerStore.state.cursorPosition.x,
          y2: lockerStore.state.cursorPosition.y,
        })
      }

      return lines
    },
  },
  methods: {
    mousemove(event) {
      let x = event.clientX - this.boxOffsetLeft
      let y = event.clientY - this.boxOffsetTop
      lockerStore.commit('move', {x, y})
    },
    touchmove(event) {
      let x = event.targetTouches[0].clientX - this.boxOffsetLeft
      let y = event.targetTouches[0].clientY - this.boxOffsetTop
      lockerStore.commit('move', {x, y})
    },
    leave() {
      if (!lockerStore.state.lockActions) {
        lockerStore.commit('resetPattern')
      }
    },
    release() {
      if (!lockerStore.state.lockActions) {
        if (lockerStore.state.showErrorOnRealse) {
          lockerStore.commit('setConnectorsColorTransition', 0.8)
          lockerStore.commit('showError')
          setTimeout(lockerStore.commit, 801, 'setConnectorsColorTransition', 0)
          setTimeout(lockerStore.commit, 1200, 'resetPattern')
        } else {
          lockerStore.commit('resetPattern')
        }
      }
    },
  },
  mounted() {
    let box = document.getElementById('draw-box')
    this.boxOffsetLeft = box.offsetLeft
    this.boxOffsetTop = box.offsetTop
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