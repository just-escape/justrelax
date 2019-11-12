<template>
  <b-card
    :header="getRoomHeader"
    header-tag="h3"
    header-class="big-noodle text-jaffa text-center"
    class="bgc-dark border-jaffa h-100"
  >
    <b-form>
      <div class="row mb-3">
        <div class="col-4 d-flex align-items-center">
          <label for="scenario" class="mb-0">Scenario</label>
        </div>
        <div class="col-8">
          <b-form-input
            id="scenario"
            v-model="scenario"
            required
            placeholder=""
          ></b-form-input>
        </div>
      </div>
      
      <div class="row mb-3">
        <div class="col-4 d-flex align-items-center">
          <label for="cardinal" class="mb-0">Cardinal</label>
        </div>
        <div class="col-8">
          <b-form-input
            id="cardinal"
            v-model="cardinal"
            required
            placeholder=""
          ></b-form-input>
        </div>
      </div>

      <div class="row">
        <div class="col-12">
          <ButtonJaffa type="submit" class="btn-block">Save</ButtonJaffa>
        </div>
      </div>
    </b-form>
  </b-card>
</template>

<script>
import ButtonJaffa from '@/components/common/ButtonJaffa.vue'
import { getRoomDisplayName } from '@/helper/room.js'
import roomStore from '@/store/roomStore.js'

export default {
  name: 'RoomRud',
  components: {
    ButtonJaffa,
  },
  data() {
    return {
      form: {
        cardinal: this.room.cardinal,
      }
    }
  },
  computed: {
    scenario: {
      get: function() {
        return this.room.scenario
      },
      set: function(value) {
        var roomId = this.room.id
        var scenario = value
        roomStore.commit("setScenario", {roomId, scenario})
      },
    },
    cardinal: {
      get: function() {
        return this.room.cardinal
      },
      set: function(value) {
        var roomId = this.room.id
        var cardinal = value
        roomStore.commit("setCardinal", {roomId, cardinal})
      },
    },
    getRoomHeader: function() {
      return getRoomDisplayName(this.room)
    }
  },
  props: ["room"]
}
</script>
