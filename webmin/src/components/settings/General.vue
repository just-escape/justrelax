<template>
  <div class="d-flex flex-column justify-content-center">
    <h2 class="big-noodle text-jaffa mb-4">General</h2>
    <b-form v-if="room">
      <div class="row mb-3">
        <div class="col-2 d-flex align-items-center">
          <label for="scenario" class="mb-0">Scenario</label>
        </div>
        <div class="col-4">
          <b-form-input
            id="scenario"
            v-model="scenario"
            required
            placeholder=""
          ></b-form-input>
        </div>
      </div>
      
      <div class="row mb-3">
        <div class="col-2 d-flex align-items-center">
          <label for="cardinal" class="mb-0">Cardinal</label>
        </div>
        <div class="col-4">
          <b-form-input
            id="cardinal"
            v-model="cardinal"
            required
            placeholder=""
          ></b-form-input>
        </div>
      </div>

      <div class="row mb-3">
        <div class="col-2 d-flex align-items-center">
          <label for="channel" class="mb-0">Channel</label>
        </div>
        <div class="col-4">
          <b-form-input
            id="channel"
            v-model="channel"
            required
            placeholder=""
          ></b-form-input>
        </div>
      </div>

      <div class="row">
        <div class="col-2 pr-0">
          <ButtonJaffa type="submit" class="btn-block">Save</ButtonJaffa>
        </div>
      </div>
    </b-form>
  </div>
</template>

<script>
import ButtonJaffa from '@/components/common/ButtonJaffa.vue'
import roomStore from '@/store/roomStore.js'

export default {
  name: 'PageSettingsGeneral',
  components: {
    ButtonJaffa,
  },
  computed: {
    scenario: {
      get: function() {
        if (this.room) {
          return this.room.scenario
        } else {
          return ""
        }
      },
      set: function(value) {
        var roomId = this.room.id
        var scenario = value
        roomStore.commit("setScenario", {roomId, scenario})
      },
    },
    cardinal: {
      get: function() {
        if (this.room) {
          return this.room.cardinal
        } else {
          return ""
        }
      },
      set: function(value) {
        var roomId = this.room.id
        var cardinal = value
        roomStore.commit("setCardinal", {roomId, cardinal})
      },
    },
    channel: {
      get: function() {
        if (this.room) {
          return this.room.channel
        } else {
          return ""
        }
      },
      set: function(value) {
        var roomId = this.room.id
        var channel = value
        roomStore.commit("setChannel", {roomId, channel})
      },
    },
    room: function() {
      return roomStore.state.rooms[this.$route.params.roomId]
    }
  },
}
</script>
