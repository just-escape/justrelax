<template>
  <div class="position-relative transition-1s" :style="{background: background, 'z-index': zIndex}">
    <i
      v-if="isPassage"
      class="position-absolute transition-1s justify-content-center d-flex align-items-center h-100 w-100 fa fa-chevron-right"
      :style="{transform: chevronTransform, opacity: displayChevron ? 1 : 0}"
      style="font-size: 100px"
    />
    <span
      v-if="isTarget"
      class="position-absolute d-flex justify-content-end align-items-end w-100 h-100 pr-1"
      style="font-size: 24px"
      :style="{opacity: numbersOpacity}"
    >
      {{ content }}
    </span>
  </div>
</template>

<script>
import sokobanStore from '@/store/sokobanStore.js'

export default {
  name: "Cell",
  computed: {
    isPassage() {
      return ['L', 'R', 'U', 'D'].includes(this.content)
    },
    isTarget() {
      return ['0', '1', '2', '3', '4', '5', '6', '7'].includes(this.content)
    },
    numbersOpacity() {
      if (this.face === 'left') {
        return sokobanStore.state.currentLevel >= 1 ? 1 : 0
      } else if (this.face === 'front') {
        return sokobanStore.state.currentLevel >= 2 ? 1 : 0
      } else {
        // top
        return sokobanStore.state.success ? 1 : 0
      }
    },
    displayChevron() {
      if (!this.isPassage) {
        return false
      } else if (this.content === 'R') {
        return this.currentLevel >= 1
      } else if (this.content === 'U') {
        return this.currentLevel >= 2
      } else {
        return true
      }
    },
    chevronTransform() {
      if (this.content === 'L') {
        return 'rotate(180deg)'
      } else if (this.content === 'U') {
        return 'rotate(270deg)'
      } else if (this.content === 'D') {
        return 'rotate(90deg)'
      } else {
        return ''
      }
    },
    background() {
      if (this.content === 'W') {
        return 'rgb(120, 120, 120)'
      } else if (this.isPassage) {
        if (this.content === 'R') {
          return this.currentLevel >= 1 ? 'darkblue' : 'rgb(120, 120, 120)'
        } else if (this.content === 'U') {
          return this.currentLevel >= 2 ? 'darkblue' : 'rgb(120, 120, 120)'
        } else {
          return 'darkblue'
        }
      } else if (this.isTarget) {
        return 'rgba(0, 209, 182, 0.3)'
      } else if (this.content === '.') {
        return 'rgba(230, 230, 230, 0)'
      } else {
        return 'rgb(0, 0, 0)'
      }
    },
    currentLevel() {
      return sokobanStore.state.currentLevel
    },
    zIndex() {
      return this.isPassage ? 10 : 0
    },
  },
  props: {
    content: String,
    face: String,
  }
}
</script>