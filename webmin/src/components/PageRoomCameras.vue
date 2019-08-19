<template>
  <div>
    <h2 class="big-noodle text-jaffa text-center">Cameras</h2>
    <div class="container-fluid">
      <div v-if="focusCam" class="row">
        <div class="col text-center px-0">
          <div class="position-absolute text-center w-100">
            {{ focusCam.name }}
          </div>
          <img
            @click="collapseFocus()"
            class="bordered pointer"
            :src="focusCam.url"
          >
        </div>
      </div>

      <div class="row">
        <div
          v-for="(cam, index) in cams"
          :key="cam.id"
          :class="getCamClasses"
        >
          <div class="position-absolute text-center w-100">
            {{ cam.name }}
          </div>
          <img
            @click="focus(index)"
            class="img-fluid pointer"
            :src="cam.url"
          >
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'PageRoomCameras',
  data: function() {
    return {
      focusCamIndex: -1,
    }
  },
  computed: {
    cams: function() {
      console.log(this.room.cams)
      return this.room.cams
    },
    getCamClasses: function() {
      var classes = ['px-0', 'bordered']
      if (this.focusCam) {
        classes.push('col')
      } else {
        classes.push('col-4')
      }
      return classes
    },
    focusCam: function() {
      if (this.focusCamIndex < 0) {
        return undefined
      } else {
        return this.cams[this.focusCamIndex]
      }
    },
  },
  methods: {
    focus: function(camIndex) {
      this.focusCamIndex = camIndex
    },
    collapseFocus: function() {
      this.focusCamIndex = -1
    }
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
