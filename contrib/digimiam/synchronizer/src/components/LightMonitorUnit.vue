<template>
  <div>
    <div
      class="position-absolute"
      :style="{
        height: width + 'px',
        width: width + 'px',
        left: trianglesPositionX + 'px',
        top: (trianglesPositionY - 18) + 'px',
        transform: 'rotate(' + trianglesRotation + ')',
      }"
    >
      <div
        class="d-flex flex-column align-items-center justify-self-center"
      >
        <LightMonitorUnitTriangle
          v-for="(t, tIndex) in triangles"
          :size="t.size"
          :opacity="t.opacity"
          :key="tIndex"
        />
      </div>
    </div>

    <svg @click="toggle" class="position-absolute" :viewBox="'0 0 ' + boxWidth + ' ' + boxHeight" :style="{width: width + 'px', top: positionY + 'px', left: positionX + 'px'}">
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
        :style="{opacity: lockerOpacity}"
      />
    </svg>
  </div>
</template>

<script>
import LightMonitorUnitTriangle from '@/components/LightMonitorUnitTriangle.vue'
import lightStore from '@/store/lightStore.js'
import justSockService from '@/store/justSockService.js'

export default {
  name: 'LightMonitorUnit',
  components: {
    LightMonitorUnitTriangle,
  },
  data: function() {
    return {
      toggled: false,
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
      },
      triangles: [
        {
          size: "lg",
          opacity: 0,
          animation: null,
          animationLoopCounter: 0,
        },
        {
          size: "md",
          opacity: 0,
          animation: null,
          animationLoopCounter: 0,
        },
        {
          size: "sm",
          opacity: 0,
          animation: null,
          animationLoopCounter: 0,
        },
      ],
      hideTriangles: false,
    }
  },
  computed: {
    blinkTriangles() {
      return lightStore.state.colorTriangles[this.color]
    },
    isActivated() {
      return lightStore.state.activatedSensors.slice(0, 4).includes(this.color)
    },
    isPressed() {
      return lightStore.state.activatedSensors.includes(this.color)
    },
    areSensorsLocked() {
      return lightStore.state.activatedSensors.length >= 4
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
  methods: {
    toggle() {
      this.toggled = !this.toggled
      lightStore.dispatch('toggleColor', {color: this.color, activated: this.toggled})
    },
    startTriangleAnimation(triangleIndex) {
      if (!this.hideTriangles) {
        this.triangles[triangleIndex].animation.play()
      }
    },
    stopTriangleAnimation() {
      this.hideTriangles = true
    },
  },
  watch: {
    blinkTriangles(value) {
      if (value) {
        this.hideTriangles = false
        this.startTriangleAnimation(0)
        setTimeout(this.startTriangleAnimation, 133, 1)
        setTimeout(this.startTriangleAnimation, 266, 2)
      } else {
        setTimeout(this.stopTriangleAnimation, 133)
      }
    },
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
        justSockService.commit('sendEvent', {"category": "on", "color": this.color})

        this.grayscaleAnimation.pause()

        this.grayscaleAnimation = this.$anime({
          targets: this,
          colorMainChannel: 1,
          colorOffChannel: 0,
          lockerOpacity: 0,
          duration: 500,
          easing: 'linear',
        })
      } else {
        justSockService.commit('sendEvent', {"category": "off", "color": this.color})

        if (this.areSensorsLocked) {
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
    let this_ = this

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

    this.triangles[0].animation = this.$anime({
      loop: true,
      direction: 'alternate',
      autoplay: false,
      duration: 399,
      update: function(anim) {
        this_.triangles[0].opacity = anim.progress * Math.min(this_.triangles[0].animationLoopCounter, 10) / 10 / 100
      },
      loopComplete: function(anim) {
        this_.triangles[0].animationLoopCounter += 1
        if (this_.hideTriangles && anim.progress === 0) {
          this_.triangles[0].animationLoopCounter = 0
          this_.triangles[0].animation.pause()
        }
      },
      easing: 'linear',
    })

    this.triangles[1].animation = this.$anime({
      loop: true,
      direction: 'alternate',
      autoplay: false,
      duration: 399,
      update: function(anim) {
        this_.triangles[1].opacity = anim.progress * Math.min(this_.triangles[1].animationLoopCounter, 10) / 10 / 100
      },
      loopComplete: function(anim) {
        this_.triangles[1].animationLoopCounter += 1
        if (this_.hideTriangles && anim.progress === 0) {
          this_.triangles[1].animationLoopCounter = 0
          this_.triangles[1].animation.pause()
        }
      },
      easing: 'linear',
    })

    this.triangles[2].animation = this.$anime({
      loop: true,
      direction: 'alternate',
      autoplay: false,
      duration: 399,
      update: function(anim) {
        this_.triangles[2].opacity = anim.progress * Math.min(this_.triangles[2].animationLoopCounter, 10) / 10 / 100
      },
      loopComplete: function(anim) {
        this_.triangles[2].animationLoopCounter += 1
        if (this_.hideTriangles && anim.progress === 0) {
          this_.triangles[2].animationLoopCounter = 0
          this_.triangles[2].animation.pause()
        }
      },
      easing: 'linear',
    })
  },
  props: {
    color: String,
    positionX: Number,
    positionY: Number,
    width: Number,
    trianglesPositionX: Number,
    trianglesPositionY: Number,
    trianglesRotation: String,
  }
}
</script>

<style scoped>
path {
  transition: all 1s linear;
}
</style>