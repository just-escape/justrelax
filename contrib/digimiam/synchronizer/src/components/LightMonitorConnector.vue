<template>
  <div
    class="connector"
    :style="{
      left: left,
      top: top,
      width: width,
      transform: transform,
      'border-top': borderTop,
    }"
  ></div>
</template>

<script>
export default {
  name: 'DishSelectorWire',
  computed: {
    left: function() {
      return ((this.x1 + this.x2) / 2) - (this.widthNoPx / 2) + 'px'
    },
    top: function() {
      return ((this.y1 + this.y2) / 2) + 'px'
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
    borderTop: function() {
      return this.thickness + 'px dashed white;'
    }
  },
  props: {
    x1: Number,
    y1: Number,
    x2: Number,
    y2: Number,
    thickness: Number,
  },
}
</script>

<style scoped>
.connector {
  position: absolute;
  opacity: 0.3;
}
</style>