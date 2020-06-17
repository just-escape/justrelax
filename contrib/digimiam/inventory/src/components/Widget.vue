<template>
  <div class="position-relative">
    <div class="position-absolute w-100 h-100 top-left">
      <div
        :class="{'text-teal': !error, 'text-orange': error}"
        class="size-20 d-flex flex-column justify-content-center align-items-center h-100 pb-3"
      >
        <i :class="icon" class="size-26px pb-1"/>
        <div v-if="error">{{ $t('error') }}</div>
        <div v-else>{{ $t('ok') }}</div>
      </div>
    </div>
    <div class="d-flex flex-column align-items-center">
      <svg
        :viewBox="'-0.75 -0.75 ' + (w + 1.5) + ' ' + (h + 1.5)"
        :class="{'svg-glowing': !error, 'svg-glowing-error': error}"
        class="mb-1"
      >
        <polygon
          :points="edges"
          :stroke="error ? 'orangered' : 'rgba(0, 209, 182, 1)'"
          stroke-width="0.75"
          fill="transparent"
        />
      </svg>
      <div>
        {{ $t(label) }}
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "Widget",
  data() {
    return {
      size: 20,
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
  props: {
    icon: String,
    status: String,
    label: String,
    error: Boolean,
  },
}
</script>

<style scoped>
.svg-glowing {
  filter: drop-shadow(0px 0px 2px rgba(0, 209, 182, 0.5));
}

.svg-glowing-error {
  filter: drop-shadow(0px 0px 2px orangered);
}

.size-26px {
  font-size: 26px;
}

.top-left {
  top: 0;
  left: 0;
}
</style>