<template>
  <div>
    <div class="container-fluid text-center">
      <!-- TODO: Implement again the focus widget, while not duplicating streams this time ^.^' -->
      <!--<div v-if="focusCamera && isFocusEnbaled" class="row">
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
      </div>-->
      <div v-if="cameras === undefined">
        Loading...
      </div>
      <div v-else class="row">
        <div v-for="camera in cameras" :key="camera.id" class="px-0 bordered col-4">
          <!-- TODO: handle the text color vs background color -->
          <!--<div class="position-absolute text-center w-100">
            {{ camera.name }} {{camera.type}}
          </div>-->
          <Camera
            v-if="camera.type === 'webrtc_janus'"
            :params="camera.params"
            :roomId="roomId"
          />
          <!--<Camera :class="getCameraClasses" :url="'http://172.16.4.102:8088/janus'" :streamId="10"/>
          <Camera :class="getCameraClasses" :url="'http://172.16.4.103:8088/janus'" :streamId="10"/>-->
        </div>
        <!-- TODO: handle MJPEG type (alongside the Janus WebRTC type) -->
        <!--<div
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
        </div>-->
      </div>
    </div>
  </div>
</template>

<script>
import Camera from '@/components/live/Camera.vue'
import notificationStore from '@/store/notificationStore.js'

export default {
  name: 'Cameras',
  components: {
    Camera,
  },
  data: function() {
    return {
      cameras: undefined,
      /*focusCameraIndex: -1,
      isFocusEnbaled: false,*/
    }
  },
  computed: {
    /*getCameraClasses: function() {
      var classes = ['px-0', 'bordered']
      /*if (this.focusCamera) {
        classes.push('col')
      } else {
        classes.push('col-4')
      // }
      return classes
    },*/
    /*focusCamera: function() {
      if (this.focusCameraIndex < 0) {
        return undefined
      } else {
        return this.cameras[this.focusCameraIndex]
      }
    },*/
  },
  /*methods: {
    focus: function(cameraIndex) {
      this.focusCameraIndex = cameraIndex
    },
    collapseFocus: function() {
      this.focusCameraIndex = -1
    },
    toggleDisplayCameras: function() {
      this.displayCameras = !this.displayCameras
    },
  },*/
  mounted() {
    let this_ = this
    this.$justRestAPI.get('/camera/?room=' + this.roomId)
      .then(function (response) {
        this_.cameras = response.data
      })
      .catch(function (error) {
        notificationStore.dispatch('pushError', 'Error while fetching cameras: ' + error)
      })
  },
  props: ['roomId']
}
</script>

<style scoped>
.z-1 {
  z-index: 1;
}
</style>
