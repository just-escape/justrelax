<template>
  <div>
    <div class="container-fluid text-center">
      <div class="row">
        <div v-for="camera in cameras.filter(camera => camera.room == roomId)" :key="camera.id" class="px-0 bordered col-4">
          <!-- TODO: handle the text color vs background color -->
          <!--<div class="position-absolute text-center w-100">
            {{ camera.name }} {{camera.type}}
          </div>-->
          <Camera
            v-if="camera.type === 'webrtc_janus'"
            :params="camera.params"
            :roomId="roomId"
          />
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

export default {
  name: 'Cameras',
  components: {
    Camera,
  },
  data: function() {
    return {
      cameras: [
        {
          "id": 1,
          "index": 0,
          "room": 1,
          "name": "d1c1",
          "type": "webrtc_janus",
          "params": "{\"url\": \"http://d1c1.justescape:8088/janus\", \"streamId\": 10, \"channel\": \"d1.c1\", \"id\": \"c1\"}"
        },
        {
          "id": 2,
          "index": 1,
          "room": 1,
          "name": "d1c2",
          "type": "webrtc_janus",
          "params": "{\"url\": \"http://d1c2.justescape:8088/janus\", \"streamId\": 10, \"channel\": \"d1.c2\", \"id\": \"c2\"}"
        },
        {
          "id": 3,
          "index": 2,
          "room": 1,
          "name": "d1c3",
          "type": "webrtc_janus",
          "params": "{\"url\": \"http://d1c3.justescape:8088/janus\", \"streamId\": 10, \"channel\": \"d1.c3\", \"id\": \"c3\"}"
        },
        {
          "id": 4,
          "index": 0,
          "room": 2,
          "name": "d2c1",
          "type": "webrtc_janus",
          "params": "{\"url\": \"http://d2c1.justescape:8088/janus\", \"streamId\": 10, \"channel\": \"d2.c1\", \"id\": \"c1\"}"
        },
        {
          "id": 5,
          "index": 1,
          "room": 2,
          "name": "d2c2",
          "type": "webrtc_janus",
          "params": "{\"url\": \"http://d2c2.justescape:8088/janus\", \"streamId\": 10, \"channel\": \"d2.c2\", \"id\": \"c2\"}"
        },
        {
          "id": 6,
          "index": 2,
          "room": 2,
          "name": "d2c3",
          "type": "webrtc_janus",
          "params": "{\"url\": \"http://d2c3.justescape:8088/janus\", \"streamId\": 10, \"channel\": \"d2.c3\", \"id\": \"c3\"}"
        }
      ],
    }
  },
  props: ['roomId']
}
</script>

<style scoped>
.z-1 {
  z-index: 1;
}
</style>
