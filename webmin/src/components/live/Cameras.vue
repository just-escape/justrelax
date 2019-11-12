<template>
  <div>
    <h2 class="big-noodle text-jaffa text-center">Cameras</h2>
    <div v-if="displayCameras" class="container-fluid">
      <div v-if="focusCamera" class="row">
        <div class="col text-center px-0">
          <div class="position-absolute text-center w-100">
            {{ focusCamera.name }}
          </div>
          <img
            @click="collapseFocus()"
            class="border-deepdark pointer"
            :src="focusCamera.url"
          >
        </div>
      </div>

      <div class="row">
        <div
          v-for="(camera, index) in room.cameras"
          :key="camera.id"
          :class="getCameraClasses"
        >
          <div class="position-absolute text-center w-100">
            {{ camera.name }}
          </div>
          <img
            @click="focus(index)"
            class="img-fluid pointer"
            :src="camera.url"
          >
        </div>
      </div>
    </div>
    <div v-else class="container-fluid text-center">
      Fetching...
    </div>
  </div>
</template>

<script>
import roomStore from '@/store/roomStore.js'

export default {
  name: 'Cameras',
  data: function() {
    return {
      focusCameraIndex: -1,
    }
  },
  computed: {
    displayCameras: function() {
      return this.room.cameras != undefined
    },
    getCameraClasses: function() {
      var classes = ['px-0', 'bordered']
      if (this.focusCamera) {
        classes.push('col')
      } else {
        classes.push('col-4')
      }
      return classes
    },
    focusCamera: function() {
      if (this.focusCameraIndex < 0) {
        return undefined
      } else {
        return this.cameras[this.focusCameraIndex]
      }
    },
  },
  methods: {
    focus: function(cameraIndex) {
      this.focusCameraIndex = cameraIndex
    },
    collapseFocus: function() {
      this.focusCameraIndex = -1
    },
    toggleDisplayCameras: function() {
      this.displayCameras = !this.displayCameras
    },
  },
  mounted() {
    roomStore.dispatch('fetchCameras', this.room.id)
  },
  props: ['room']
}
</script>

<style scoped>
.z-1 {
  z-index: 1;
}
</style>
