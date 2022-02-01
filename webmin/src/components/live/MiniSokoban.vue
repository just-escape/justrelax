<template>
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
      <MiniSokobanLevel
        :sceneSize="sceneSize"
        :transform="transformLeft"
        :face="'left'"
      />
      <MiniSokobanLevel
        :sceneSize="sceneSize"
        :transform="transformFront"
        :face="'front'"
      />
      <MiniSokobanLevel
        :sceneSize="sceneSize"
        :transform="transformTop"
        :face="'top'"
      />
    </div>
  </div>
</template>

<script>
import MiniSokobanLevel from '@/components/live/MiniSokobanLevel.vue'

export default {
  name: "MiniSokoban",
  components: {
    MiniSokobanLevel,
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
    cubeSize() {
      return this.sceneSize + 'px'
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
    cubeTransform() {
      return 'translateZ(' + (- this.sceneSize / 2) + 'px) rotateX(' + this.cubeRotateX + 'deg) rotateY(' + this.cubeRotateY + 'deg)'
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
  props: [
    'currentFace',
    'currentLevel',
  ],
}
</script>

<style scoped>
.cube {
  transform-style: preserve-3d;
}
.transition-1s {
  transition: all 1s;
}
</style>