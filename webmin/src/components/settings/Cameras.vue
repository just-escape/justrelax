<template>
  <div class="d-flex flex-column justify-content-center">
    <h2 class="big-noodle text-jaffa mb-4">Cameras</h2>
    <div v-for="(c, index) in cameras" :key="c.id" class="mb-4">
      <CameraRud
        :chevronUp="!isFirstCamera(index)"
        :chevronDown="!isLastCamera(index)"
        :cameraIndex="index"
      />
    </div>
    <div class="mb-4">
      <CameraCreate :nCameras="nCameras"/>
    </div>
  </div>
</template>

<script>
import CameraRud from '@/components/settings/CameraRud.vue'
import CameraCreate from '@/components/settings/CameraCreate.vue'
import roomStore from '@/store/roomStore.js'

export default {
  name: 'Cameras',
  components: {
    CameraRud,
    CameraCreate,
  },
  computed: {
    cameras: function() {
      if (this.room == undefined) {
        return []
      } else if (this.room.cameras == undefined) {
        return []
      } else {
        return this.room.cameras
      }
    },
    nCameras: function() {
      return this.cameras.length
    },
    isFirstCamera: function() {
      return function(cameraIndex) {
        return cameraIndex == 0
      }
    },
    isLastCamera: function() {
      return function(cameraIndex) {
        return cameraIndex == Object.keys(this.cameras).length - 1
      }
    },
    room: function() {
      if (roomStore.state.rooms.length == 0) {
        return {}
      } else {
        return roomStore.state.rooms[this.$route.params.roomId]
      }
    }
  },
  mounted() {
    roomStore.watch(
      (state) => state.rooms,
      () => {
        roomStore.dispatch('fetchCameras', this.room.id)
      }
    )
  },
}
</script>
