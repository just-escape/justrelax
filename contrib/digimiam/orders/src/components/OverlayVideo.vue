<template>
  <div>
    <video v-if="displayOverlayVideo" :src="overlayVideoId" mute autoplay @ended="onEnd()"></video>
  </div>
</template>

<script>
import videoStore from '@/store/videoStore.js'

export default {
  name: "OverlayVideo",
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
}
</script>

<style scoped>
video {
  display: block; /* Removes a mysterious margin bottom */
}
</style>
