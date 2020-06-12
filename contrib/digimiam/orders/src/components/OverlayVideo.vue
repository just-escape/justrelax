<template>
  <div>
    <video
      v-if="displayVideo"
      :src="src"
      :loop="loop"
      autoplay
      @ended="onEnd()"
    />
  </div>
</template>

<script>
import progressionStore from '@/store/progressionStore.js'

export default {
  name: "OverlayVideo",
  data() {
    return {
      // Is updated only when a video is not playing
      videoLang: this.$i18n.locale,
    }
  },
  computed: {
    displayVideo() {
      return progressionStore.state.currentOverlayVideo !== null
    },
    src() {
      if (this.displayVideo) {
        return progressionStore.state.overlayVideos[progressionStore.state.currentOverlayVideo][this.videoLang]
      } else {
        return ""
      }
    },
    loop() {
      if (this.displayVideo) {
        return progressionStore.state.overlayVideos[progressionStore.state.currentOverlayVideo].loop
      } else {
        return false
      }
    },
    locale() {
      return this.$i18n.locale
    },
  },
  methods: {
    onEnd() {
      progressionStore.commit('onOverlayVideoEnd')
      this.videoLang = this.locale
    },
  },
  watch: {
    locale(newValue) {
      if (!this.displayVideo) {
        // Otherwise, wait for the onEnd callback to update
        this.videoLang = newValue
      }
    },
  },
}
</script>
