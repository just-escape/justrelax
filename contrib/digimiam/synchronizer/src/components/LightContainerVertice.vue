<template>
  <g>
    <g v-if="!startingPoint" :class="{'d-none': hidePulses}">
      <polygon
        v-for="(p, pulseIndex) in pulses" :key="pulseIndex"
        :fill="getFill(p.opacity)"
        :points="getEdges(verticeDiameter * p.scale)"
      />
    </g>
    <polygon
      :fill="getFill(a)"
      :stroke="stroke"
      :points="getEdges(startingPoint ? verticeDiameter * 0.87 : verticeDiameter)"
      :filter="'url(#' + glowing + ')'"
    />
  </g>
</template>

<script>
export default {
  name: 'LightContainerVertice',
  data: function () {
    return {
      verticeDiameter: 32,
      hidePulses: false,
      pulses: [
        {
          animation: null,
          opacity: 0.4,
          scale: 1,
        },
        {
          animation: null,
          opacity: 0.4,
          scale: 1,
        },
        {
          animation: null,
          opacity: 0.4,
          scale: 1,
        },
      ],
    }
  },
  computed: {
    getH: function() {
      return function(diameter) {
        var h = Math.sqrt(3 * diameter * diameter / 16)
        return h
      }
    },
    getW: function() {
      return function(diameter) {
        var w = diameter / 2
        return w
      }
    },
    getEdges: function() {
      return function(diameter) {
        var centerX = this.x
        var centerY = this.y

        var leftX = centerX - this.getW(diameter)
        var leftY = centerY

        var topLeftX = centerX - this.getW(diameter) / 2
        var topLeftY = centerY - this.getH(diameter)

        var topRightX = centerX + this.getW(diameter) / 2
        var topRightY = centerY - this.getH(diameter)

        var rightX = centerX + this.getW(diameter)
        var rightY = centerY

        var bottomRightX = centerX + this.getW(diameter) / 2
        var bottomRightY = centerY + this.getH(diameter)

        var bottomLeftX = centerX - this.getW(diameter) / 2
        var bottomLeftY = centerY + this.getH(diameter)

        return leftX + ',' + leftY + ' ' + topLeftX + ',' + topLeftY + ' ' + topRightX + ',' + topRightY + ' ' + rightX + ',' + rightY + ' ' + bottomRightX + ',' + bottomRightY + ' ' + bottomLeftX + ',' + bottomLeftY
      }
    },
    getFill: function() {
      return function(opacity) {
        if (this.startingPoint) {
          return 'rgba(0, 0, 0, 0)'
        } else {
          if (this.showGlobalError) {
            return 'rgba(255, 20, 40)'
          } else {
            return 'rgba(' + this.r + ', ' + this.g + ', ' + this.b + ', ' + opacity + ')'
          }
        }
      }
    },
    stroke: function() {
      if (this.startingPoint) {
        if (this.showGlobalError) {
          return 'rgba(255, 20, 40)'
        } else {
          return 'rgba(' + this.r + ', ' + this.g + ', ' + this.b + ', ' + this.a + ')'
        }
      } else {
        return 'rgba(0, 0, 0, 0)'
      }
    },
  },
  methods: {
    startPulseAnimation(pulseIndex) {
      if (this.pulse) {
        this.pulses[pulseIndex].animation.play()
      }
    },
    stopAllPulseAnimation() {
      this.hidePulses = true
    },
  },
  watch: {
    pulse: function(newValue) {
      if (newValue) {
        this.hidePulses = false
        this.startPulseAnimation(0)
        setTimeout(this.startPulseAnimation, 325, 1)
        setTimeout(this.startPulseAnimation, 650, 2)
      } else {
        setTimeout(this.stopAllPulseAnimation, 325)
      }
    }
  },
  mounted() {
    let this_ = this

    this.pulses[0].animation = this.$anime.timeline({
      targets: this_.pulses[0],
      loop: true,
      autoplay: false,
      duration: 975,
      loopComplete: function() {
        this_.pulses[0].opacity = 0.4
        this_.pulses[0].scale = 1
        if (this_.hidePulses) {
          this_.pulses[0].animation.pause()
        }
      },
    })
    .add({
      scale: 3,
      easing: 'linear',
    })
    .add({
      opacity: 0.03,
      easing: 'linear',
    }, '-=975')

    this.pulses[1].animation = this.$anime.timeline({
      targets: this_.pulses[1],
      loop: true,
      autoplay: false,
      duration: 975,
      loopComplete: function() {
        this_.pulses[1].opacity = 0.4
        this_.pulses[1].scale = 1
        if (this_.hidePulses) {
          this_.pulses[1].animation.pause()
        }
      },
    })
    .add({
      scale: 3,
      easing: 'linear',
    })
    .add({
      opacity: 0.03,
      easing: 'linear',
    }, '-=975')

    this.pulses[2].animation = this.$anime.timeline({
      targets: this_.pulses[2],
      loop: true,
      autoplay: false,
      duration: 975,
      loopComplete: function() {
        this_.pulses[2].opacity = 0.4
        this_.pulses[2].scale = 1
        if (this_.hidePulses) {
          this_.pulses[2].animation.pause()
        }
      },
    })
    .add({
      scale: 3,
      easing: 'linear',
    })
    .add({
      opacity: 0.03,
      easing: 'linear',
    }, '-=975')
  },
  props: {
    x: Number,
    y: Number,
    startingPoint: Boolean,
    r: Number,
    g: Number,
    b: Number,
    a: Number,
    showGlobalError: Boolean,
    glowing: String,
    pulse: Boolean,
  }
}
</script>

<style scoped>
polygon {
  stroke-width: 6px;
}
</style>