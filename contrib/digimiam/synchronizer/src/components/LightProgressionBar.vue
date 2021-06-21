<template>
  <div class="w-100">
    <div
      class="position-relative glowing-container overflow-hidden"
      style="height: 60px; transition: filter 4s ease-in-out"
      :style="{filter: success ? 'hue-rotate(-40deg) brightness(0.65) contrast(0.95)' : ''}"
    >
      <div
        class="h-100"
        :style="{width: realProgression + '%'}"
      />
      <div class="position-absolute w-100" style="height: 58px; top: 0">
        <div
          ref="displayedProgressionBar"
          class="h-100 d-inline-block"
          style="background-color: rgb(0, 209, 182)"
        />
        <div
          ref="decrementBar"
          class="h-100 d-inline-block"
          style="transform: translateX(calc(-100% + 1px)); background-color: #ff4500"
        />
      </div>
    </div>
  </div>
</template>

<script>
import lightStore from '@/store/lightStore.js'

export default {
  name: 'LightProgressionBar',
  data() {
    return {
      ticTask: undefined,
      isDisplayedProgressionBarFilling: false,
    }
  },
  computed: {
    realProgression() {
      return lightStore.state.progression
    },
    success() {
      return lightStore.state.success
    },
  },
  methods: {
    tic() {
      if (!lightStore.state.success) {
        lightStore.commit('progress', -1)
        this.ticTask = setTimeout(this.tic, 1500)
      }
    },
  },
  watch: {
    realProgression(newValue, oldValue) {
      let ticTaskDelay = 1500
      let fillingDelay = 100
      if (this.isDisplayedProgressionBarFilling) {
        ticTaskDelay -= 100
        fillingDelay -= 100
      }

      clearTimeout(this.ticTask)
      this.ticTask = setTimeout(this.tic, ticTaskDelay)
      this.isDisplayedProgressionBarFilling = true
      let this_ = this
      this.$anime({
        targets: this.$refs.displayedProgressionBar,
        delay: fillingDelay,
        duration: 1400,
        width: newValue + '%',
        easing: 'easeOutQuint',
        complete: () => {
          this_.isDisplayedProgressionBarFilling = false
        }
      })

      if (newValue < oldValue) {
        this.$refs.decrementBar.style.width = (oldValue - newValue) + '%'
        this.$anime({
          targets: this.$refs.decrementBar,
          delay: fillingDelay,
          duration: 1200,
          width: '0%',
          easing: 'easeOutQuint',
        })
      }
    },
  },
  mounted() {
    this.$refs.displayedProgressionBar.style.width = this.realProgression + '%'
  }
}
</script>
