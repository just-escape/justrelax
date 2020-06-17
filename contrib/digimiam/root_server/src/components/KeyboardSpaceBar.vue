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
      :viewBox="'-0.75 -0.75 ' + (3.25 * w + 1.5) + ' ' + (1.5 * h + 1.5)"
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
        {{ character }}
      </div>
    </div>
  </div>
</template>

<script>
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
      var ax = this.w / 4
      var ay = this.h / 2

      var bX = 3 * this.w / 4
      var bY = this.h / 2

      var cX = this.w
      var cY = 0

      var dX = 3 * this.w / 2
      var dY = 0

      var eX = 7 * this.w / 4
      var eY = this.h / 2

      var fX = 9 * this.w / 4 + 1
      var fY = this.h / 2

      var gX = 10 * this.w / 4 + 1
      var gY = 0

      var hX = 12 * this.w / 4 + 1
      var hY = 0

      var iX = 13 * this.w / 4 + 1
      var iY = this.h / 2

      var jX = 12 * this.w / 4 + 1
      var jY = this.h

      var kX = 10 * this.w / 4 + 1
      var kY = this.h

      var lX = 9 * this.w / 4 + 1
      var lY = 6 * this.h / 4

      var mX = 7 * this.w / 4
      var mY = 6 * this.h / 4

      var nX = 6 * this.w / 4
      var nY = this.h

      var oX = this.w
      var oY = this.h

      var pX = 3 * this.w / 4
      var pY = 6 * this.h / 4

      var qX = this.w / 4
      var qY = 6 * this.h / 4

      var rX = 0
      var rY = this.h

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
        lX + ',' + lY + ' ' +
        mX + ',' + mY + ' ' +
        nX + ',' + nY + ' ' +
        oX + ',' + oY + ' ' +
        pX + ',' + pY + ' ' +
        qX + ',' + qY + ' ' +
        rX + ',' + rY
      )
    },
  },
  methods: {
    press() {
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
</style>