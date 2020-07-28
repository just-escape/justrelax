<template>
  <div class="w-100 h-100 pointer-events-none">
    <div
      class="position-absolute w-100 h-100 top-left bg-black transition-4s pointer-events-none"
      :style="{opacity: blackScreenOpacity}"
    />
    <video
      v-if="displayVideo"
      class="position-absolute"
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
      blackScreenOpacity: 1,
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
    displayVideo(newValue) {
      if (newValue) {
        this.blackScreenOpacity = 1
      } else {
        this.blackScreenOpacity = 0
      }
    },
  },
}
</script>

<style scoped>
.top-left {
  top: 0px;
  left: 0px;
}

.bg-black {
  background: black;
}

.transition-4s {
  transition: all 4s ease-in-out;
}

.pointer-events-none {
  pointer-events: none;
}
</style>
