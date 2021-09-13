<template>
  <div
    @mousedown="press"
    @touchstart="press"
    class="position-absolute"
    :style="{
      top: top + 'px',
      left: left + 'px',
      width: width + 'px',
      transform: 'scale(' + scale + ')',
    }"
  >
    <svg :viewBox="'-0.75 -0.75 ' + (w + 1.5) + ' ' + (h + 1.5)" class="svg-glowing">
      <polygon
        :points="edges"
        :stroke="'rgba(0, 209, 182, 1)'"
        stroke-width="0.75"
        :fill="'rgba(0, 209, 182, ' + fillOpacity + ')'"
      />
    </svg>
    <div class="position-absolute w-100 h-100 top-left">
      <div class="size-20 d-flex justify-content-center align-items-center h-100">
        {{ character }}
      </div>
    </div>
  </div>
</template>

<script>
import businessStore from '@/store/businessStore.js'

export default {
  name: "KeyboardLetter",
  data() {
    return {
      size: 20,
      scale: 1,
      fillOpacity: 0,
      preventRepeat: false,
    }
  },
  computed: {
    h() {
      return Math.sqrt(3) * this.size
    },
    w() {
      return 2 * this.size
    },
    edges() {
      var leftX = 0
      var leftY = this.h / 2

      var topLeftX = 0.25 * this.w
      var topLeftY = 0

      var topRightX = 0.75 * this.w
      var topRightY = 0

      var rightX = this.w
      var rightY = this.h / 2

      var bottomRightX = 0.75 * this.w
      var bottomRightY = this.h

      var bottomLeftX = 0.25 * this.w
      var bottomLeftY = this.h

      return leftX + ',' + leftY + ' ' + topLeftX + ',' + topLeftY + ' ' + topRightX + ',' + topRightY + ' ' + rightX + ',' + rightY + ' ' + bottomRightX + ',' + bottomRightY + ' ' + bottomLeftX + ',' + bottomLeftY
    },
  },
  methods: {
    allowRepeat() {
      this.preventRepeat = false
    },
    press() {
      if (businessStore.state.displayPasswordWindow || businessStore.state.displayPasswordRecoveryWindow) {
        if (this.preventRepeat) {
          return
        }

        this.preventRepeat = true
        setTimeout(this.allowRepeat, 200)

        this.$anime.timeline({
          targets: this,
        })
        .add({
          scale: 1.2,
          fillOpacity: 0.2,
          duration: 175,
          easing: 'easeOutSine',
        })
        .add({
          scale: 1,
          fillOpacity: 0,
          duration: 175,
          easing: 'easeInSine',
        })

        businessStore.commit('press', this.character)
      }
    },
  },
  props: {
    top: Number,
    left: Number,
    width: Number,
    character: String,
  },
}
</script>