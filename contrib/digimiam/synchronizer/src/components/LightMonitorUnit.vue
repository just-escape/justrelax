<template>
  <svg :viewBox="'0 0 ' + boxWidth + ' ' + boxHeight" class="position-absolute" :style="{top: positionY, left: positionX}">
    <defs>
      <filter :id="'mu-glowing-' + color" x="-50" y="-50" width="150" height="150">
        <feGaussianBlur result="blurOut" in="offOut" :stdDeviation="glowIntensity"/>
        <feBlend in="SourceGraphic" in2="blurOut" mode="normal"/>
      </filter>
      <filter :id="'mu-grayscale-' + color">
        <feColorMatrix
          type="matrix"
          :values="grayscaleMatrix"
        />
      </filter>
      <filter id="locker">
        <feImage :xlink:href="require('@/assets/img/locker.png')"/>
      </filter>
    </defs>

    <g :filter="'url(#mu-glowing-' + color + ')'">
      <path
        :key="colorMainChannel"
        :d="getEdges(size)"
        :fill="fill"
        :filter="'url(#mu-grayscale-' + color + ')'"
      />
    </g>
    <rect
      x="42.5%" y="41.5%" width="16%" height="16%"
      filter="url(#locker)"
      :style="{opacity: 0.7}"
    />
  </svg>
</template>

<script>
import lightStore from '@/store/lightStore.js'

export default {
  name: 'LightMonitorUnit',
  data: function() {
    return {
      boxWidth: 250,
      boxHeight: 250,
      size: 40,
      glowIntensity: 0,
      glowIntensityAnimation: null,
      colorMainChannel: 1,
      colorOffChannel: 0,
      grayscaleAnimation: null,
      lockerOpacity: 0,
      colors: {
        pink: {
          r: 232,
          g: 62,
          b: 140,
        },
        white: {
          r: 255,
          g: 255,
          b: 255,
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
        red: {
          r: 220,
          g: 53,
          b: 69,
        },
      }
    }
  },
  computed: {
    isActivated() {
      return lightStore.state.activatedSensors.slice(0, 3).includes(this.color)
    },
    isPressed() {
      return lightStore.state.activatedSensors.includes(this.color)
    },
    areSensorsLocked() {
      return lightStore.state.activatedSensors.length >= 3
    },
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
    getEdges: function() {
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
    grayscaleMatrix() {
      return this.colorMainChannel + ' ' + this.colorOffChannel + ' ' + this.colorOffChannel + ' 0 0 ' + this.colorOffChannel + ' ' +  this.colorMainChannel + ' ' + this.colorOffChannel + ' 0 0 ' + this.colorOffChannel + ' ' + this.colorOffChannel + ' ' + this.colorMainChannel + ' 0 0 0 0 0 1 0'
    },
    fill() {
      var r = this.colors[this.color].r
      var g = this.colors[this.color].g
      var b = this.colors[this.color].b
      return 'rgba(' + r + ', ' + g + ', ' + b + ')'
    }
  },
  watch: {
    isPressed(newValue) {
      this.glowIntensityAnimation.pause()

      if (newValue) {
        this.glowIntensityAnimation = this.$anime({
          targets: this,
          glowIntensity: 25,
          duration: 500,
          easing: 'easeOutQuad',
        })
      } else {
        this.glowIntensityAnimation = this.$anime({
          targets: this,
          glowIntensity: 0,
          duration: 500,
          easing: 'easeOutQuad',
        })
      }
    },
    isActivated(newValue) {
      if (newValue) {
        this.grayscaleAnimation.pause()

        this.grayscaleAnimation = this.$anime({
          targets: this,
          colorMainChannel: 1,
          colorOffChannel: 0,
          lockerOpacity: 0,
          duration: 500,
          easing: 'linear',
        })
      } else if (this.areSensorsLocked) {
        this.grayscaleAnimation.pause()

        this.grayscaleAnimation = this.$anime({
          targets: this,
          colorMainChannel: 0.33,
          colorOffChannel: 0.33,
          lockerOpacity: 0.7,
          duration: 500,
          easing: 'linear',
        })
      }
    },
    areSensorsLocked(newValue) {
      if (newValue) {
        if (!this.isActivated) {
          this.grayscaleAnimation.pause()

          this.grayscaleAnimation = this.$anime({
            targets: this,
            colorMainChannel: 0.33,
            colorOffChannel: 0.33,
            lockerOpacity: 0.7,
            duration: 500,
            easing: 'linear',
          })
        }
      } else {
        this.grayscaleAnimation.pause()

        this.grayscaleAnimation = this.$anime({
          targets: this,
          colorMainChannel: 1,
          colorOffChannel: 0,
          lockerOpacity: 0,
          duration: 500,
          easing: 'linear',
        })
      }
    },
  },
  created() {
    this.grayscaleAnimation = this.$anime({
      targets: this,
      autoplay: false,
      colorMainChannel: 0.33,
      colorOffChannel: 0.33,
      lockerOpacity: 0.7,
      duration: 1000,
      easing: 'linear',
    })
    this.glowIntensityAnimation = this.$anime({
      targets: this,
      autoplay: false,
      glowIntensity: 0,
      duration: 500,
      easing: 'linear',
    })
  },
  props: {
    color: String,
    positionX: Number,
    positionY: Number,
  }
}
</script>

<style scoped>
path {
  transition: all 1s linear;
}
</style>