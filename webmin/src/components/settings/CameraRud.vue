<template>
  <div class="row">
    <div class="col-2 d-flex align-items-center pr-0">
      <b-img
        :src="url"
        class="img-fluid border-deepdark"
        :blank="url == ''"
        blank-color="#3c3c3e"
      />
    </div>
    <div class="col-4">
      <b-form>
        <div class="row mb-3">
          <div class="col-3 align-items-center d-flex">
            <label for="name" class="mb-0">Name</label>
          </div>
          <div class="col-9">
            <b-form-input
              id="name"
              v-model="name"
              required
              :placeholder="namePlaceholder"
            ></b-form-input>
          </div>
        </div>

        <div class="row">
          <div class="col-3 align-items-center d-flex">
            <label for="url" class="mb-0">URL</label>
          </div>
          <div class="col-9">
            <b-form-input
              id="url"
              v-model="url"
              required
              placeholder="https://..."
            ></b-form-input>
          </div>
        </div>
      </b-form>
    </div>

    <div class="col-2 d-flex align-items-center justify-content-end">
      <b-button-group class="mr-3">
        <ButtonJaffa :disabled="!chevronUp">
          <i class="fas fa-chevron-up"></i>
        </ButtonJaffa>
        <ButtonJaffa :disabled="!chevronDown">
          <i class="fas fa-chevron-down"></i>
        </ButtonJaffa>
      </b-button-group>

      <ButtonJaffa>
        <i class="fas fa-times"></i>
      </ButtonJaffa>
    </div>
  </div>
</template>

<script>
import ButtonJaffa from '@/components/common/ButtonJaffa.vue'
import roomStore from '@/store/roomStore.js'

export default {
  name: 'CameraRud',
  components: {
    ButtonJaffa,
  },
  computed: {
    namePlaceholder: function() {
      return 'Cam ' + (this.cameraIndex + 1)
    },
    name: {
      get: function() {
        if (this.camera == undefined) {
          return ''
        } else {
          return this.room.cameras[this.cameraIndex].name
        }
      },
      set: function(value) {
        if (this.camera != undefined) {
          var roomId = this.room.id
          var cameraIndex = this.cameraIndex
          var name = value
          roomStore.commit("setCameraName", {roomId, cameraIndex, name})
        }
      }
    },
    url: {
      get: function() {
        if (this.camera == undefined) {
          return ''
        } else {
          return this.room.cameras[this.cameraIndex].url
        }
      },
      set: function(value) {
        if (this.camera != undefined) {
          var roomId = this.room.id
          var cameraIndex = this.cameraIndex
          var url = value
          roomStore.commit("setCameraURL", {roomId, cameraIndex, url})
        }
      }
    },
    room: function() {
      if (roomStore.state.rooms.length == 0) {
        return undefined
      } else {
        return roomStore.state.rooms[this.$route.params.roomId]
      }
    },
    camera: function() {
      if (this.room == undefined) {
        return undefined
      }

      if (this.room.cameras == undefined) {
        return undefined
      }

      return this.room.cameras[this.cameraIndex]
    }
  },
  props: ["chevronUp", "chevronDown", "cameraIndex"]
}
</script>
