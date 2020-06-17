<template>
  <Window :title="$t('stock_management')">
    <div class="d-flex flex-column align-items-center justify-content-around h-100">
      <div
        class="transition-1s"
        :style="{
          perspective: scenePerspective,
          'perspective-origin': scenePerspectiveOrigin,
        }"
      >
        <div
          class="position-relative cube transition-1s"
          :style="{width: cubeSize, height: cubeSize, transform: cubeTransform}"
        >
          <Level
            :sceneSize="sceneSize"
            :transform="transformLeft"
            :face="'left'"
          />
          <Level
            :sceneSize="sceneSize"
            :transform="transformFront"
            :face="'front'"
          />
          <Level
            :sceneSize="sceneSize"
            :transform="transformTop"
            :face="'top'"
          />
        </div>
      </div>

    </div>
  </Window>
</template>

<script>
import Window from '@/components/Window.vue'
import Level from '@/components/Level.vue'
import sokobanStore from '@/store/sokobanStore.js'

export default {
  name: "Sokoban",
  components: {
    Window,
    Level,
  },
  data() {
    return {
      sceneSize: 800,
    }
  },
  computed: {
    scenePerspective() {
      return this.sceneSize * 5 + 'px'
    },
    scenePerspectiveOrigin() {
      return this.scenePerspectiveOriginX + '% ' + this.scenePerspectiveOriginY + '%'
    },
    transformLeft() {
      return 'rotateY(-90deg) translateZ(' + this.sceneSize / 2 + 'px)'
    },
    transformFront() {
      return 'translateZ(' + this.sceneSize / 2 + 'px)'
    },
    transformTop() {
      return 'rotateX(90deg) translateZ(' + this.sceneSize / 2 + 'px)'
    },
    cubeSize() {
      return this.sceneSize + 'px'
    },
    cubeTransform() {
      return 'translateZ(' + (- this.sceneSize / 2) + 'px) rotateX(' + this.cubeRotateX + 'deg) rotateY(' + this.cubeRotateY + 'deg)'
    },
    currentFace() {
      return sokobanStore.state.currentFace
    },
    currentLevel() {
      return sokobanStore.state.currentLevel
    },
    cubeRotateX() {
      if (this.currentFace === 'top') {
        return -90
      } else {
        return 0
      }
    },
    cubeRotateY() {
      if (this.currentFace === 'left') {
        return 90
      } else {
        return 0
      }
    },
    scenePerspectiveOriginX() {
      if (this.currentFace === 'left') {
        if (this.currentLevel > 0) {
          return 130
        } else {
          return 100
        }
      } else if (this.currentFace === 'front') {
        if (this.currentLevel > 1) {
         return -30
        } else {
          return -30
        }
      } else if (this.currentFace === 'top') {
        return -30
      } else {
        return -30
      }
    },
    scenePerspectiveOriginY() {
      if (this.currentFace === 'left') {
        if (this.currentLevel > 1) {
          return -20
        } else {
          return 0
        }
      } else if (this.currentFace === 'front') {
        if (this.currentLevel > 1) {
         return -20
        } else {
          return 0
        }
      } else if (this.currentFace === 'top') {
        return 120
      } else {
        return 120
      }
    },
  },
  methods: {
    move(direction) {
      sokobanStore.commit('move', direction)
    },
    keypress(e) {
      if (e.code === "KeyA") {
        sokobanStore.commit('move', "left")
      } else if (e.code === "KeyS") {
        sokobanStore.commit('move', "down")
      } else if (e.code === "KeyD") {
        sokobanStore.commit('move', "right")
      } else if (e.code === "KeyW") {
        sokobanStore.commit('move', 'up')
      }
    },
    reset() {
      sokobanStore.commit('reset')
    },
  },
  mounted() {
    window.addEventListener('keypress', (e) => this.keypress(e))
  }
}
</script>

<style scoped>
.cube {
  transform-style: preserve-3d;
}
</style>