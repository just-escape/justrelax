<template>
  <div
    class="position-relative scene d-flex align-items-center justify-content-center"
    v-touch:swipe.left="swipeLeft"
    v-touch:swipe.right="swipeRight"
    v-touch:swipe.top="swipeTop"
    v-touch:swipe.bottom="swipeBottom"
  >
    <div class="position-absolute w-100 d-flex flex-row" style="bottom: 0px; left: 0px">
      <b-btn @click="setLevel(0)">Level 1</b-btn>
      <b-btn @click="setLevel(1)">Level 2</b-btn>
      <b-btn @click="setLevel(2)">Level 3</b-btn>
    </div>

    <div
      class="scene"
      :style="{
        perspective: scenePerspective,
        'perspective-origin': scenePerspectiveOrigin,
      }"
    >
      <div
        class="position-relative cube"
        :style="{width: cubeSize, height: cubeSize, transform: cubeTransform}"
      >
        <Level
          :transform="transformLeft"
          :map="mapLeft"
        />
        <Level
          :transform="transformFront"
          :map="mapFront"
        />
        <Level
          :transform="transformTop"
          :map="mapTop"
        />
      </div>
    </div>
  </div>
</template>

<script>
import Level from '@/components/Level.vue'
import sokobanStore from '@/store/sokobanStore.js'

export default {
  name: "Sokoban",
  components: {
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
    mapLeft() {
      return sokobanStore.state.currentGrids.left
    },
    mapFront() {
      return sokobanStore.state.currentGrids.front
    },
    mapTop() {
      return sokobanStore.state.currentGrids.top
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
    setFace(face) {
      sokobanStore.commit('setFace', face)
    },
    setLevel(level) {
      sokobanStore.commit('setLevel', level)
    },
    swipeLeft() {
      if (this.currentFace === 'left' && this.currentLevel > 0) {
        sokobanStore.commit('setFace', 'front')
      }
    },
    swipeRight() {
      if (this.currentFace === 'front') {
        sokobanStore.commit('setFace', 'left')
      } else if (this.currentFace === 'top') {
        sokobanStore.commit('setFace', 'left')
      }
    },
    swipeTop() {
      if (this.currentFace === 'top') {
        sokobanStore.commit('setFace', 'front')
      }
    },
    swipeBottom() {
      if (this.currentFace !== 'top' && this.currentLevel > 1) {
        sokobanStore.commit('setFace', 'top')
      }
    },
  },
}
</script>

<style scoped>
.scene {
  transition: all 1s;
}

.cube {
  transform-style: preserve-3d;
  transition: all 1s;
}
</style>