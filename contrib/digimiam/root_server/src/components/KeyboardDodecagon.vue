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
    <svg
      :viewBox="'-0.75 -0.75 ' + (7 * w / 4 + 1.5) + ' ' + (2 * h + 1.5)"
      class="svg-glowing"
      :class="{'rotate-180': mirror}"
    >
      <polygon
        :points="edges"
        :stroke="'rgba(0, 209, 182, 1)'"
        stroke-width="0.75"
        :fill="'rgba(0, 209, 182, ' + fillOpacity + ')'"
      />
    </svg>
    <div class="position-absolute w-100 h-100 top-left">
      <div class="size-20 d-flex justify-content-center align-items-center h-100">
        <i v-if="character === 'BACKSPACE'" class="size-22 fas fa-backspace"></i>
        <i v-else-if="character === 'CR'" class="size-22 cr fa fa-reply"></i>
        <span v-else>{{ character }}</span>
      </div>
    </div>
  </div>
</template>

<script>
import keyboardStore from '@/store/keyboardStore.js'

export default {
  name: "KeyboardDodecagon",
  data() {
    return {
      size: 20,
      scale: 1,
      fillOpacity: 0,
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
      var ax = 0
      var ay = this.h / 2

      var bX = this.w / 4
      var bY = 0

      var cX = 3 * this.w / 4
      var cY = 0

      var dX = this.w
      var dY = this.h / 2

      var eX = 6 * this.w / 4
      var eY = this.h / 2

      var fX = 7 * this.w / 4
      var fY = this.h

      var gX = 6 * this.w / 4
      var gY = 6 * this.h / 4

      var hX = this.w
      var hY = 6 * this.h / 4

      var iX = 3 * this.w / 4
      var iY = 2 * this.h

      var jX = this.w / 4
      var jY = 2 * this.h

      var kX = 0
      var kY = 6 * this.h / 4

      var lX = 0.25 * this.w
      var lY = this.h

      return (
        ax + ',' + ay + ' ' +
        bX + ',' + bY + ' ' +
        cX + ',' + cY + ' ' +
        dX + ',' + dY + ' ' +
        eX + ',' + eY + ' ' +
        fX + ',' + fY + ' ' +
        gX + ',' + gY + ' ' +
        hX + ',' + hY + ' ' +
        iX + ',' + iY + ' ' +
        jX + ',' + jY + ' ' +
        kX + ',' + kY + ' ' +
        lX + ',' + lY
      )
    },
  },
  methods: {
    press() {
      if (keyboardStore.state.displayPasswordWindow || keyboardStore.state.displayPasswordRecoveryWindow) {
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

        if (this.character === 'BACKSPACE') {
          keyboardStore.commit('backspace')
        } else if (this.character === 'CR') {
          keyboardStore.commit('cr')
        }
      }
    },
  },
  props: {
    top: Number,
    left: Number,
    width: Number,
    character: String,
    mirror: Boolean,
  },
}
</script>

<style scoped>
.rotate-180 {
  transform: rotate(180deg);
}

.cr {
  transform: scaleY(-1);
}

.size-22 {
  font-size: 22px;
}
</style>