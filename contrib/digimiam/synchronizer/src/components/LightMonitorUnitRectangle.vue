<template>
  <div class="position-relative">
    <svg :viewBox="'0 0 ' + boxWidth + ' ' + boxHeight" :style="{width: (this.vertical ? this.longEdge / 1.618 : this.longEdge) + 'px'}">
      <defs>
        <filter :id="'mu-glowing-' + color" x="-50" y="-50" width="150" height="150">
          <feGaussianBlur result="blurOut" in="offOut" :stdDeviation="glowIntensity"/>
          <feBlend in="SourceGraphic" in2="blurOut" mode="normal"/>
        </filter>
      </defs>

      <g :filter="'url(#mu-glowing-' + color + ')'">
        <path
          :d="getEdges(size)"
          :fill="fill"
        />
      </g>
      <polygon
        fill="rgba(0, 0, 0, 0)"
        stroke="rgba(0, 209, 182, 0.7)"
        stroke-width="3.5" 
        :points="getPoints(size)"
        filter="url(#glowing-rectangle)"
      />
    </svg>
  </div>
</template>

<script>
import lightStore from '@/store/lightStore.js'

export default {
  name: 'LightMonitorUnitRectangle',
  data: function() {
    return {
      size: 90,
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
          glowIntensity: 10,
        },
        green: {
          r: 40,
          g: 167,
          b: 69,
          glowIntensity: 18,
        },
        blue: {
          r: 0,
          g: 123,
          b: 255,
          glowIntensity: 18,
        },
        orange: {
          r: 253,
          g: 126,
          b: 20,
          glowIntensity: 18,
        },
        red: {
          r: 220,
          g: 53,
          b: 69,
          glowIntensity: 25,
        },
      },
    }
  },
  computed: {
    isActivated() {
      return lightStore.state.activatedSensors[this.color]
    },
    boxHeight() {
      return this.vertical ? 1.618 * 150 : 1.1 * 150
    },
    boxWidth() {
      return this.vertical ? 1.1 * 150 : 1.618 * 150
    },
    h() {
      return function(size) {
        return this.vertical ? 1.618 * size : 1.1 * size
      }
    },
    w() {
      return function(size) {
        return this.vertical ? 1.1 * size : 1.618 * size
      }
    },
    corner() {
      return function(size) {
        return 0.2 * size
      }
    },
    getEdges() {
      return function(size) {
        var topLeftRight = "M" + (this.boxWidth / 2 - 0.5 * this.w(size) + this.corner(size)) + " " + (this.boxHeight / 2 - 0.5 * this.h(size))
        var topRightLeft = "h" + (this.w(size) - 2 * this.corner(size))
        var topRightBottom = "l" + (this.corner(size) + " " + this.corner(size))
        var bottomRightTop = "v" + (this.h(size) - 2 * this.corner(size))
        var bottomRightLeft = "l" + -1 * this.corner(size) + " " + this.corner(size)
        var bottomLeftRight = "h" + -1 * (this.w(size) - 2 * this.corner(size))
        var bottomLeftTop = "l" + -1 * this.corner(size) + " " + -1 * this.corner(size)
        var topLeftBottom = "v" + (-1 * (this.h(size) - 2 * this.corner(size)))
        return topLeftRight + " " + topRightLeft + " " + topRightBottom + " " + bottomRightTop + " " + bottomRightLeft + " " + bottomLeftRight + " " + bottomLeftTop + " " + topLeftBottom
      }
    },
    getPoints() {
      return function(size) {
        var topLeftRight = (this.boxWidth / 2 - 0.5 * this.w(size) + this.corner(size)) + "," + (this.boxHeight / 2 - 0.5 * this.h(size))
        var topRightLeft = (this.boxWidth / 2 + 0.5 * this.w(size) - this.corner(size)) + "," + (this.boxHeight / 2 - 0.5 * this.h(size))
        var topRightBottom = (this.boxWidth / 2 + 0.5 * this.w(size)) + "," + (this.boxHeight / 2 - 0.5 * this.h(size) + this.corner(size))
        var bottomRightTop = (this.boxWidth / 2 + 0.5 * this.w(size)) + "," + (this.boxHeight / 2 + 0.5 * this.h(size) - this.corner(size))
        var bottomRightLeft = (this.boxWidth / 2 + 0.5 * this.w(size) - this.corner(size)) + "," + (this.boxHeight / 2 + 0.5 * this.h(size))
        var bottomLeftRight = (this.boxWidth / 2 - 0.5 * this.w(size) + this.corner(size)) + "," + (this.boxHeight / 2 + 0.5 * this.h(size))
        var bottomLeftTop = (this.boxWidth / 2 - 0.5 * this.w(size)) + "," + (this.boxHeight / 2 + 0.5 * this.h(size) - this.corner(size))
        var topLeftBottom = (this.boxWidth / 2 - 0.5 * this.w(size)) + "," + (this.boxHeight / 2 - 0.5 * this.h(size) + this.corner(size))
        return topLeftRight + " " + topRightLeft + " " + topRightBottom + " " + bottomRightTop + " " + bottomRightLeft + " " + bottomLeftRight + " " + bottomLeftTop + " " + topLeftBottom
      }
    },
    fill() {
      if (this.isActivated) {
        var r = this.colors[this.color].r
        var g = this.colors[this.color].g
        var b = this.colors[this.color].b
        return 'rgba(' + r + ', ' + g + ', ' + b + ')'
      } else {
        return 'rgba(0, 0, 0, 0)'
      }
    },
    glowIntensity() {
      return this.colors[this.color].glowIntensity
    },
  },
  props: {
    color: String,
    longEdge: Number,
    vertical: Boolean,
    triggerOnOffPublications: Boolean,
  }
}
</script>

<style scoped>
path {
  transition: all 1s linear;
}
</style>