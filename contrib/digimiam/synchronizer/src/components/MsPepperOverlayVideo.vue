<template>
  <div>
    <video
      v-if="displayVideo"
      :src="src"
      autoplay
      @ended="onEnd()"
    />
  </div>
</template>

<script>
import progressionStore from '@/store/progressionStore.js'

export default {
  name: "MsPepperOverlayVideo",
  computed: {
    displayVideo() {
      return progressionStore.state.currentMsPepperOverlayVideo !== null
    },
    src() {
      if (this.displayVideo) {
        return progressionStore.state.msPepperOverlayVideos[progressionStore.state.currentMsPepperOverlayVideo].media
      } else {
        return ""
      }
    },
    loop() {
      if (this.displayVideo) {
        return progressionStore.state.msPepperOverlayVideos[progressionStore.state.currentMsPepperOverlayVideo].loop
      } else {
        return false
      }
    },
  },
  methods: {
    onEnd() {
      progressionStore.commit('stopMsPepperOverlayVideo')
    },
  },
}
</script>