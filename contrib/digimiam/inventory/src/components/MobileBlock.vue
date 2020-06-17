<template>
  <div class="transition-400ms clip-path-hexagon" :style="{background: background}"></div>
</template>

<script>
import sokobanStore from '@/store/sokobanStore.js'

export default {
  name: "MobileBlock",
  computed: {
    background() {
      if (this.areBlocksFrozen) {
        return 'lightgreen'
      } else if (['0', '1', '2', '3', '4', '5', '6', '7'].includes(sokobanStore.state.grids[sokobanStore.state.difficulty][this.face][this.y][this.x])) {
        return 'green'
      } else {
        return 'saddlebrown'
      }
    },
    areBlocksFrozen() {
      if (this.face === 'left') {
        return sokobanStore.state.currentLevel >= 1
      } else if (this.face === 'front') {
        return sokobanStore.state.currentLevel >= 2
      } else {
        // top
        return sokobanStore.state.success
      }
    },
  },
  props: {
    face: String,
    x: Number,
    y: Number,
  }
}
</script>

<style scoped>
.clip-path-hexagon-100 {
  clip-path: polygon(
    0% 50%,
    25% 6.7%,
    75% 6.7%,
    100% 50%,
    75% 93.3%,
    25% 93.3%
  );
}

.clip-path-hexagon-80 {
  clip-path: polygon(
    10% 50%,
    30% 15%,
    70% 15%,
    90% 50%,
    70% 85%,
    30% 85%
  );
}

.clip-path-hexagon {
  clip-path: polygon(
    15% 50%,
    32.5% 19.7%,
    67.5% 19.7%,
    85% 50%,
    67.5% 80.3%,
    32.5% 80.3%
  );
}
</style>