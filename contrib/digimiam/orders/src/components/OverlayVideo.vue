<template>
  <div>
    <video v-if="displayOverlayVideo" :src="cutscene" mute autoplay @ended="onEnd()"></video>
  </div>
</template>

<script>
import progressionStore from '@/store/progressionStore.js'

export default {
  name: "OverlayVideo",
  computed: {
    displayOverlayVideo() {
      return progressionStore.state.currentCutscene !== undefined
    },
    cutscene() {
      return progressionStore.state.cutscenes[progressionStore.state.currentCutscene]
    },
  },
  methods: {
    onEnd() {
      progressionStore.commit('onCutsceneEnd')
    },
  },
}
</script>

<style scoped>
video {
  display: block; /* Removes a mysterious margin bottom */
}
</style>
