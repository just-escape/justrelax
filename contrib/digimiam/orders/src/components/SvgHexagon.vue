<template>
  <svg :viewBox="'0 0 ' + boxWidth + ' ' + boxHeight">
    <defs>
      <filter id="glowing" x="-50" y="-50" width="150" height="150">
        <feGaussianBlur result="blurOut" in="offOut" stdDeviation="20"/>
        <feBlend in="SourceGraphic" in2="blurOut" mode="normal"/>
      </filter>
    </defs>

    <path
      :d="d(size)"
      fill="#00d1b6"
      filter="url('#glowing')"
    />
  </svg>
</template>

<script>
export default {
  name: 'SvgHexagon',
  data: function() {
    return {
      boxWidth: 150,
      boxHeight: 150,
      size: 40,
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
  },
}
</script>