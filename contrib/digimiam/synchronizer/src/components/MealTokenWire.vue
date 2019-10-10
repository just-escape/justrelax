<template>
  <div
    class="wire"
    :style="{left: left, top: top, width: width, transform: transform, height: thickness, zIndex: zIndex}"
  ></div>
</template>

<script>
import MenuStore from '@/store/MenuStore.js'

export default {
  name: 'MealTokenWire',
  data: function() {
    return {
      thicknessNoPx: 1,
    }
  },
  computed: {
    x1: function() {
      return this.token.cursorLeft + this.token.cursorWidth / 2
    },
    y1: function() {
      return this.token.cursorTop + this.token.cursorHeight / 2
    },
    x2: function() {
      return this.token.wireX2
    },
    y2: function() {
      return this.token.wireY2
    },
    left: function() {
      return ((this.x1 + this.x2) / 2) - (this.widthNoPx / 2) + 'px'
    },
    top: function() {
      return ((this.y1 + this.y2) / 2) - (this.thicknessNoPx / 2) + 'px'
    },
    thickness: function() {
      return this.thicknessNoPx + 'px'
    },
    widthNoPx: function() {
      return Math.sqrt(
        (
          (this.x2 - this.x1) * (this.x2 - this.x1)
        ) + (
          (this.y2 - this.y1) * (this.y2 - this.y1)
        )
      )
    },
    width: function() {
      return this.widthNoPx + 'px'
    },
    transform: function() {
      var angle = Math.atan2((this.y1 - this.y2), (this.x1 - this.x2)) * (180 / Math.PI)
      return 'rotate(' + angle + 'deg)'
    },
    zIndex: function() {
      return this.token.zIndex
    },
    token: function() {
      return MenuStore.state.tokens[this.tokenIndex]
    },
  },
  props: ['tokenIndex'],
}
</script>

<style scoped>
.wire {
  position: absolute;
  background-color: #00d1b6;
  box-shadow: 0px 1px 3px 0.01px rgba(0, 209, 182, 0.7);
}
</style>