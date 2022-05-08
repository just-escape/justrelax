<template>
  <div
    class="w-100 h-100 z-index-50 position-absolute"
    style="top: 0; left: 0; transition: all 1s ease-in-out; background: black"
    :class="{'d-none': !display}"
  >
  </div>
</template>

<script>
import progressionStore from '@/store/progressionStore.js'

export default {
  name: "BlackScreen",
  computed: {
    display() {
      return progressionStore.state.displayBlackScreen
    },
  },
}
</script>
