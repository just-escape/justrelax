<template>
  <div>
    <video v-if="displayOverlayVideo" :src="cutscene" autoplay @ended="onEnd()"></video>
  </div>
</template>

<script>
import progressionStore from '@/store/progressionStore.js'

export default {
  name: "OverlayVideo",
  data() {
    return {
      // Is updated only when a cutscene is not playing
      cutsceneLang: this.$i18n.locale,
    }
  },
  computed: {
    displayOverlayVideo() {
      return progressionStore.state.currentCutscene !== undefined
    },
    cutscene() {
      return progressionStore.state.cutscenes[progressionStore.state.currentCutscene][this.cutsceneLang]
    },
    locale() {
      return this.$i18n.locale
    },
  },
  methods: {
    onEnd() {
      progressionStore.commit('onCutsceneEnd')
      this.cutsceneLang = this.locale
    },
  },
  watch: {
    locale(newValue) {
      if (!this.displayOverlayVideo) {
        // Otherwise, wait for the onEnd callback to update
        this.cutsceneLang = newValue
      }
    },
  },
}
</script>

<style scoped>
video {
  display: block; /* Removes a mysterious margin bottom */
}
</style>
