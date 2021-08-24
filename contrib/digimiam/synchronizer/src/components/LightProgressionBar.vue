<template>
  <div class="position-relative w-100 d-flex flex-row" :style="{filter: hueRotate ? 'hue-rotate(-40deg) brightness(0.65) contrast(0.95)' : '', 'transition': 'filter 4s ease-in-out'}">
    <Lightning
      :intensity="realProgression / 100"
      class="position-absolute w-100" :style="{opacity: hueRotate ? 0 : 1}" style="top: -150px; left: 0px; z-index: 0; height: 240px; transition: opacity 4s ease-in-out"
    />
    <div class="d-flex flex-row justify-content-center align-items-center h-100" style="width: 70px; background: rgba(0, 94, 110, 1); z-index: 0">
      <div style="font-size: 30px; color: #031a22" class="fas fa-bolt"></div>
    </div>
    <div
      class="position-relative overflow-hidden w-100"
      style="height: 60px; transition: filter 4s ease-in-out; border: 1px solid; border-image-slice: 1"
      :style="{
        'border-image-source': 'linear-gradient(to right, rgba(0, 94, 110, 1) ' + progressionBarContainerTenPercent + 'px, rgba(0, 209, 182, 1) ' + progressionBarContainerNinetyPercent + 'px)',
      }"
    >
      <div
        class="h-100"
        :style="{width: realProgression + '%', background: 'linear-gradient(to right, rgba(0, 94, 110, 0.3) ' + progressionBarContainerTenPercent + 'px, rgba(0, 209, 182, 0.3) ' + progressionBarContainerNinetyPercent + 'px)'}"
      />
      <div ref="progressionBarContainer" class="position-absolute w-100" style="height: 58px; top: 0">
        <div
          ref="displayedProgressionBar"
          class="h-100 d-inline-block"
          :style="{background: 'linear-gradient(to right, rgba(0, 94, 110, 1) ' + progressionBarContainerTenPercent + 'px, rgba(0, 209, 182, 1) ' + progressionBarContainerNinetyPercent + 'px)'}"
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
import Lightning from '@/components/Lightning.vue'
import lightStore, { EASY, HARD } from '@/store/lightStore.js'

export default {
  name: 'LightProgressionBar',
  components: {
    Lightning,
  },
  data() {
    return {
      didPlayersProgressed: false,
      ticTask: undefined,
      ticCombo: 0,
      isDisplayedProgressionBarFilling: false,
      progressionBarContainerTenPercent: 0,
      progressionBarContainerNinetyPercent: 0,
      hueRotate: false,
    }
  },
  computed: {
    realProgression() {
      return lightStore.state.progression
    },
    success() {
      return lightStore.state.success
    },
    lightDifficulty() {
      return lightStore.state.difficulty 
    }
  },
  methods: {
    tic() {
      if (!lightStore.state.success) {
        this.ticCombo++
        let progressMalus
        let nextTicDelay
        if (this.lightDifficulty === EASY) {
          progressMalus = -1
          nextTicDelay = 3000
        } else if (this.lightDifficulty === HARD) {
          if (this.ticCombo >= 0) {
            progressMalus = -1 * Math.exp(this.ticCombo)
          } else {
            progressMalus = -1
          }
          nextTicDelay = 1500
        } else {
          // NORMAL
          progressMalus = -1
          nextTicDelay = 1500
        }
        lightStore.commit('progress', progressMalus)
        this.ticTask = setTimeout(this.tic, nextTicDelay)
      }
    },
    setHasProgressionRecentlyIncreasedFalse() {
      this.hasProgressionRecentlyIncreased = false
    },
    setHueRotateTrue() {
      this.hueRotate = true
    }
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
      } else {
        this.ticCombo = -3
        this.didPlayersProgressed = true
      }
    },
    success(newValue) {
      if (newValue) {
        setTimeout(this.setHueRotateTrue, 3000)
      }
    }
  },
  mounted() {
    this.$refs.displayedProgressionBar.style.width = this.realProgression + '%'
    this.progressionBarContainerTenPercent = this.$refs.progressionBarContainer.offsetWidth * 0.1
    this.progressionBarContainerNinetyPercent = this.$refs.progressionBarContainer.offsetWidth * 0.9
  }
}
</script>
