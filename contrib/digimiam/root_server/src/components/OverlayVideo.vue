<template>
  <div class="position-absolute top-left z-index-20">
    <video
      v-if="displayVideo"
      :src="src"
      autoplay
      @ended="onEnd()"
    />
  </div>
</template>

<script>
import businessStore from '@/store/businessStore.js'

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
      return businessStore.state.currentOverlayVideo !== null
    },
    src() {
      if (this.displayVideo) {
        return businessStore.state.overlayVideos[businessStore.state.currentOverlayVideo][this.videoLang]
      } else {
        return ""
      }
    },
    locale() {
      return this.$i18n.locale
    },
  },
  methods: {
    onEnd() {
      businessStore.commit('onOverlayVideoEnd')
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
