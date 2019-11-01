<template>
  <div>
    <svg :viewBox="'0 0 ' + boxWidth + ' ' + boxHeight">
      <defs>
        <filter id="mu-glowing" x="-50" y="-50" width="150" height="150">
          <feGaussianBlur result="blurOut" in="offOut" stdDeviation="20"/>
          <feBlend in="SourceGraphic" in2="blurOut" mode="normal"/>
        </filter>
      </defs>

      <path
        :d="d(sizeColor)"
        :fill="getColor"
        :filter="filter"
      />
    </svg>
  </div>
</template>

<script>
export default {
  name: 'LightMonitorUnit',
  data: function() {
    return {
      boxWidth: 135,
      boxHeight: 135,
      sizeColor: 40,
      sizeContainer: 50,
      colors: {
        pink: {
          r: 232,
          g: 62,
          b: 140,
        },
        yellow: {
          r: 255,
          g: 193,
          b: 7,
        },
        green: {
          r: 40,
          g: 167,
          b: 69,
        },
        blue: {
          r: 0,
          g: 123,
          b: 255,
        },
        orange: {
          r: 253,
          g: 126,
          b: 20,
        },
        purple: {
          r: 102,
          g: 16,
          b: 242,
        },
      }
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
    filter() {
      if (this.on) {
        return "url(#mu-glowing)"
      } else {
        return ""
      }
    },
    getColor() {
      var ratio = 1
      if (!this.on) {
        ratio = 0.6
      }
      var r = this.colors[this.color].r * ratio
      var g = this.colors[this.color].g * ratio
      var b = this.colors[this.color].b * ratio
      return 'rgb(' + r + ', ' + g + ', ' + b + ')'
    }
  },
  props: ['color', 'on']
}
</script>