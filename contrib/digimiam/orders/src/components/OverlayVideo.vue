<template>
  <div>
    <video v-if="displayOverlayVideo" :src="overlayVideoId" mute autoplay class="overlay" @ended="onEnd()"></video>
  </div>
</template>

<script>
import videoStore from '@/store/videoStore.js'

export default {
  name: "Scene",
  computed: {
    displayOverlayVideo() {
      return videoStore.state.overlayVideoId !== undefined
    },
    overlayVideoId() {
      if (videoStore.state.overlayVideoId === 'video1') {
        return require('@/assets/hologram.mp4')
      } else {
        return require('@/assets/cambraisienne_boucle.mp4')
      }
    },
  },
  methods: {
    onEnd() {
      videoStore.commit('setOverlayVideoId', undefined)
    },
  },
  watch: {
    overlayVideoId() {
      console.log('hey')
    }
  }
}
</script>

<style scoped>
video {
  display: block; /* Removes a mysterious margin bottom */
}
</style>