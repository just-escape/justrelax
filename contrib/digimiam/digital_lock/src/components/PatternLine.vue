<template>
  <div
    class="position-absolute"
    :style="{
      left: left,
      top: top,
      width: width,
      transform: transform,
      height: thickness,
      background: background,
      transition: transition,
    }"
  ></div>
</template>

<script>
import lockStore from '@/store/lockStore.js'

export default {
  name: 'PatternLine',
  data() {
    return {
      thicknessNoPx: 12,
    }
  },
  computed: {
    left() {
      return ((this.x1 + this.x2) / 2) - (this.widthNoPx / 2) + 'px'
    },
    top() {
      return ((this.y1 + this.y2) / 2) - (this.thicknessNoPx / 2) + 'px'
    },
    thickness() {
      return this.thicknessNoPx + 'px'
    },
    widthNoPx() {
      return Math.sqrt(
        (
          (this.x2 - this.x1) * (this.x2 - this.x1)
        ) + (
          (this.y2 - this.y1) * (this.y2 - this.y1)
        )
      )
    },
    width() {
      return this.widthNoPx + 'px'
    },
    transform() {
      var angle = Math.atan2((this.y1 - this.y2), (this.x1 - this.x2)) * (180 / Math.PI)
      return 'rotate(' + angle + 'deg)'
    },
    background() {
      return 'rgba(' + lockStore.state.connectorsColor.r + ', ' + lockStore.state.connectorsColor.g + ', ' + lockStore.state.connectorsColor.b + ', 0.5)'
    },
    transition() {
      return 'background ' + lockStore.state.connectorsColorTransition + 's ease-out'
    },
  },
  props: {
    x1: Number,
    y1: Number,
    x2: Number,
    y2: Number,
  },
}
</script>