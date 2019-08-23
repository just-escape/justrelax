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
            class="bordered pointer"
            :src="focusCamera.url"
          >
        </div>
      </div>

      <div class="row">
        <div
          v-for="(camera, index) in cameras"
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
import justRestAPI from '@/store/justRestService.js'

export default {
  name: 'PageRoomCameras',
  data: function() {
    return {
      focusCameraIndex: -1,
      displayCameras: false,
      cameras: [],
    }
  },
  computed: {
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
    filterCameras: function(response) {
      if (response.data.success) {
        var cameras = response.data.content
        cameras.map(function(camera) {
          if (this.room.cameras.includes(camera.id)) {
            this.cameras.push(camera)
          }
        }, this)
      } else {
        // eslint-disable-next-line
        console.error(response.data.error)
      }
    },
  },
  mounted() {
    justRestAPI.get('/cameras')
      .then(
        this.filterCameras
      )
      .catch(function (error) {
        // eslint-disable-next-line
        console.error(error)
      })
      .finally(
        this.toggleDisplayCameras
      )
  },
  props: ['room']
}
</script>

<style scoped>
.bordered {
  border: 1px #2e2e2e solid;
}

.z-1 {
  z-index: 1;
}
</style>
