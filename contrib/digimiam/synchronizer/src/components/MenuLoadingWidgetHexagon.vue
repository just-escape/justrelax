<template>
  <svg :viewBox="'0 0 ' + boxWidth + ' ' + boxHeight" class="position-absolute" :style="{top: positionY, left: positionX}">
    <path
      :d="d(size)"
      :fill="getFill"
    />
  </svg>
</template>

<script>
export default {
  name: 'MenuLoadingWidgetHexagon',
  data: function() {
    return {
      boxWidth: 140,
      boxHeight: 140,
      size: 65,
      animation: null,
      opacity: 0,
    }
  },
  computed: {
    h: function() {
      return function(size) {
        return Math.sqrt(3) * size
      }
    },
    w: function() {
      return function(size) {
        return 2 * size
      }
    },
    d: function() {
      return function(size) {
        var center = "M" + this.boxWidth / 2 + " " + this.boxHeight / 2
        var p1 = "m" + (-0.25 * this.w(size)) + " " + (-0.5 * this.h(size))
        var p2 = "h" + 0.5 * this.w(size)
        var p3 = "l" + 0.25 * this.w(size) + " " + 0.5 * this.h(size)
        var p4 = "l" + (-0.25 * this.h(size)) + " " + 0.5 * this.h(size)
        var p5 = "h" + (-0.5 * this.w(size))
        var p6 = "l" + (-0.25 * this.w(size)) + " " + (-0.5 * this.h(size))
        return center + " " + p1 + " " + p2 + " " + p3 + " " + p4 + " " + p5 + " " + p6
      }
    },
    getFill: function() {
      var opacity
      if (this.blinkAnimation) {
        opacity = this.opacity
      } else {
        opacity = 1
      }

      if (this.color === 'green') {
        return 'rgba(0, 170, 0, ' + opacity + ')'
      } else if (this.color === 'red') {
        return 'rgba(255, 0, 0, ' + opacity + ')'
      } else {
        return 'rgba(255, 255, 255, ' + opacity + ')'
      }
    },
  },
  watch: {
    blinkAnimation(newValue) {
      if (newValue) {
        this.animation = this.$anime.timeline({
          targets: this,
          loop: true,
          duration: 300,
          easing: 'linear',
        })
        .add({
          opacity: 1,
        })
        .add({
          opacity: 0,
          endDelay: 250,  // Should be 300 in theory but 250 looks smooth
        })
      } else {
        this.opacity = 0
        this.animation.pause()
      }
    }
  },
  props: {
    positionX: {
      type: Number,
      required: true,
    },
    positionY: {
      type: Number,
      required: true,
    },
    color: {
      type: String,
      default: 'white',
    },
    blinkAnimation: {
      type: Boolean,
      default: false,
    },
  }
}
</script>