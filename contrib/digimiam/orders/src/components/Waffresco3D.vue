<template>
  <div class="p-3" :style="'width: 250px; height: 250px; overflow: hidden; -webkit-mask-image: radial-gradient(circle at 0 0, black ' + transparencyFactor + '%, transparent ' + (transparencyFactor + 60) + '%);'">
    <div
      class="position-relative w-100 h-100"
      style="transform: rotateX(-24deg) rotateY(32deg); transform-style: preserve-3d"
    >
      <div class="position-absolute w-100 h-100" :style="{transform: 'translate3d(' + waffrescoX + 'px,' + waffrescoY + 'px, 0px)'}">
        <div class="position-relative w-100 h-100" style="overflow: hidden; border: 3px rgba(120, 42, 42, 0.67) solid; border-radius: 50%; background-color: orange">
            <div class="position-absolute d-flex flex-column justify-content-between h-100 w-100" style="top: 0; left: 0">
              <div
                v-for="index in 13" :key="index"
                style="height: 30px; width: 100%; background: linear-gradient(to bottom, rgba(165, 42, 42, 0) 0%, rgba(165, 42, 42, 0.4) 70%, rgba(165, 42, 42, 0.4) 80%, rgba(165, 42, 42, 0) 100%)"
              />
            </div>
            <div class="position-absolute d-flex flex-row justify-content-between h-100 w-100" style="top: 0; left: 0">
              <div
                v-for="index in 13" :key="index"
                style="height: 100%; width: 30px; background: linear-gradient(to right, rgba(165, 42, 42, 0) 0%, rgba(165, 42, 42, 0.4) 70%, rgba(165, 42, 42, 0.4) 80%, rgba(165, 42, 42, 0) 100%)"
              />
            </div>
        </div>
      </div>
      <div
        class="position-absolute w-100 h-100"
        :style="{transform: 'translate3d(' + dotsX + 'px, ' + dotsY + 'px, 10px'}"
      >
        <WaffrescoDot v-for="i in 6" :key="i" :left="getDotLeft(i)" :top="getDotTop(i)"/>
        <WaffrescoDot :left="109" :top="109"/>
      </div>
      <div
        class="position-absolute d-flex flex-row justify-content-center align-items-center w-100 h-100"
        :style="{transform: 'translate3d(' + patternX + 'px, ' + patternY + 'px, 20px)'}"
      >
        <img style="transform: scale(1.3)" src="@/assets/img/M.svg">
      </div>
    </div>
  </div>
</template>

<script>
import WaffrescoDot from '@/components/WaffrescoDot.vue'

export default {
  name: "Waffresco3D",
  components: {
    WaffrescoDot,
  },
  data() {
    return {
      hasAnimationEnterBeenPlayed: false,
      transparencyFactor: 0,
      waffrescoX: 240,
      waffrescoY: 240,
      dotsX: 245,
      dotsY: 245,
      patternX: 250,
      patternY: 250,
    }
  },
  methods: {
    getDotLeft(dotIndex) {
      return 218 / 2 + 85 * Math.cos(Math.PI / 180 * (60 * (dotIndex + 1) - 30))
    },
    getDotTop(dotIndex) {
      return 218 / 2 + 85 * Math.sin(Math.PI / 180 * (60 * (dotIndex + 1) - 30))
    },
    waffrescoFloatAnimation() {
      this.$anime.timeline({
        targets: this,
        loop: true,
        duration: 2500,
        direction: 'alternate',
        easing: 'easeInOutSine',
      })
      .add({
        waffrescoY: 2,
      })
      .add({
        waffrescoY: -2,
      })
    },
    dotsFloatAnimation() {
      this.$anime.timeline({
        targets: this,
        loop: true,
        duration: 2000,
        direction: 'alternate',
        easing: 'easeInOutSine',
      })
      .add({
        dotsY: -2,
      })
      .add({
        dotsY: 2,
      })
    },
    patternFloatAnimation() {
      this.$anime.timeline({
        targets: this,
        loop: true,
        duration: 1800,
        direction: 'alternate',
        easing: 'easeInOutSine',
      })
      .add({
        patternY: -2,
      })
      .add({
        patternY: 2,
      })
    },
    waffrescoAnimationEnter() {
      this.hasAnimationEnterBeenPlayed = true
      let this_ = this
      this.$anime.timeline({
        targets: this,
        delay: 500,
        complete: this_.waffrescoFloatAnimation,
      })
      .add({
        waffrescoX: 0,
        waffrescoY: 0,
        easing: 'easeOutSine',
        duration: 2000,
      })

      this.$anime.timeline({
        targets: this,
        delay: 1500,
        complete: this_.dotsFloatAnimation,
      })
      .add({
        dotsX: 5,
        dotsY: 5,
        easing: 'easeOutSine',
        duration: 2000,
      })

      this.$anime.timeline({
        targets: this,
        delay: 2500,
        complete: this_.patternFloatAnimation,
      })
      .add({
        patternX: 10,
        patternY: 10,
        easing: 'easeOutSine',
        duration: 2000,
      })

      this.$anime.timeline({
        targets: this,
      })
      .add({
        delay: 1500,
        transparencyFactor: 40,
        easing: 'easeOutSine',
        duration: 2000,
      })
      .add({
        transparencyFactor: 100,
        easing: 'easeOutSine',
        duration: 2000,
      })
    }
  },
  watch: {
    display(newValue) {
      if (newValue && !this.hasAnimationEnterBeenPlayed) {
        this.waffrescoAnimationEnter()
      }
    }
  },
  props: {
    display: Boolean
  },
}
</script>