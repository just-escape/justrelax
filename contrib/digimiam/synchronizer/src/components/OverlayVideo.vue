<template>
  <div>
    <video
      v-if="displayVideo"
      :src="src"
      loop
      autoplay
    />
  </div>
</template>

<script>
import progressionStore from '@/store/progressionStore.js'

export default {
  name: "OverlayVideo",
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
    videoLang() {
      if (this.$i18n.locale === 'fr') {
        return 'fr'
      } else {
        return 'en'
      }
    },
  },
}
</script>