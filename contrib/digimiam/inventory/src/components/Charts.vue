<template>
  <div>
    <svg viewBox="-3 -3 112 59" class="mb-1">
      <path d="M2,0 2,53"/>
      <path d="M-2,49.5 106,49.5"/>

      <foreignObject
        width="100%"
        height="100%"
        :x="$i18n.locale == 'fr' ? '-13' : '-17'"
        y="21"
        transform="rotate(-90 -5 20)"
      >
        <body xmlns="http://www.w3.org/1999/xhtml" class="bg-transparent">
          <div class="label">
            {{ $t('kcal_unit') }}.{{ $t('h_unit') }}<sup>-1</sup>.{{ $t('inhab_unit') }}<sup>-1</sup>
          </div>
        </body>
      </foreignObject>

      <foreignObject
        width="100%"
        height="100%"
        x="99"
        y="50"
      >
        <body xmlns="http://www.w3.org/1999/xhtml" class="bg-transparent">
          <div class="label">
            {{ $t('age') }}
          </div>
        </body>
      </foreignObject>

      <circle
        v-for="p in points"
        :key="p.id"
        :cx="p.x"
        :cy="p.y"
        r="0.3"
      />
      <path
        v-for="(p, index) in points.slice(0, -1)"
        :key="p.id"
        :d="getBezier(index)"
      />
    </svg>
    <div class="title text-center">
      {{ $t('feeling_of_hunger') }}
    </div>
  </div>
</template>

<script>
export default {
  name: 'Charts',
  data: function() {
    return {
      points: [
        {x: 10, y: 42},
        {x: 20, y: 44},
        {x: 30, y: 44},
        {x: 40, y: 40},
        {x: 50, y: 32.5},
        {x: 60, y: 19},
        {x: 70, y: 4},
        {x: 80, y: 12},
        {x: 90, y: 38},
        {x: 100, y: 39},
      ],
    }
  },
  computed: {
    getBezier() {
      return function(pointIndex) {
        var cps = this.controlPoint(this.points[pointIndex], this.points[pointIndex - 1], this.points[pointIndex + 1])
        var cpe = this.controlPoint(this.points[pointIndex + 1], this.points[pointIndex], this.points[pointIndex + 2], true)

        return 'M' + this.points[pointIndex].x + ',' + this.points[pointIndex].y + ' C' + cps.x + ',' + cps.y + ' ' + cpe.x + ',' + cpe.y + ' ' + this.points[pointIndex + 1].x + ',' + this.points[pointIndex + 1].y
      }
    },
  },
  methods: {
    line: function(p1, p2) {
      var lengthX = p2.x - p1.x
      var lengthY = p2.y - p1.y

      return {
        length: Math.sqrt(Math.pow(lengthX, 2) + Math.pow(lengthY, 2)),
        angle: Math.atan2(lengthY, lengthX),
      }
    },
    controlPoint: function(current, previous, next, reverse) {
      var p = previous || current
      var n = next || current

      var smoothing = 0.2

      var o = this.line(p, n)

      var angle = o.angle + (reverse ? Math.PI : 0)
      var length = o.length * smoothing

      var x = current.x + Math.cos(angle) * length
      var y = current.y + Math.sin(angle) * length
      return {'x': x, 'y': y}
    },
    variation: function(valueIndex) {
      // between -20.0% and +20.0%
      var newVariation = Math.floor(Math.random() * 400 - 200) / 10

      if (newVariation != 0) {
        if (
          this.points[valueIndex].y * (1 + (newVariation / 100)) > 47 ||
          this.points[valueIndex].y * (1 + (newVariation / 100)) < 2
        ) {
          newVariation *= -1
        }

        this.$anime({
          targets: this.points[valueIndex],
          y: this.points[valueIndex].y * (1 + (newVariation / 100)),
          duration: 3000,
          easing: 'easeInSine',
        })
      }

      setTimeout(this.variation, Math.random() * 5000 + 9000, valueIndex)
    }
  },
  mounted: function() {
    for (var i = 0 ; i < this.points.length ; i++) {
      this.variation(i)
    }
  },
}
</script>

<style scoped>
svg {
  height: 132px;
  width: 264px;
  border: 1px solid rgba(00, 209, 182, 0.4);
  box-shadow: 0px 0px 10px -6px rgba(0, 209, 182, 0.75);
}

.title {
  font-size: 12px;
}

circle {
  stroke: #00f1b6;
  fill: #00f1b6;
}

path {
  stroke: #00f1b6;
  stroke-width: 0.5;
  fill: transparent;
}

.label {
  font-family: "Code New Roman";
  color: #ffffff;
  font-size: 4px;
  display: inline-block;
  position: absolute;
  top: 0;
}
</style>
