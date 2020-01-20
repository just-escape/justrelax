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
          {{ room.scenario }}
        </div>
      </div>
      
      <div class="row mb-3">
        <div class="col-4 d-flex align-items-center">
          <label for="cardinal" class="mb-0">Cardinal</label>
        </div>
        <div class="col-8">
          {{ room.cardinal }}
        </div>
      </div>
    </b-form>
  </b-card>
</template>

<script>
import { getRoomDisplayName } from '@/helper/room.js'

export default {
  name: 'RoomRead',
  data() {
    return {
      form: {
        cardinal: this.room.cardinal,
      }
    }
  },
  computed: {
    getRoomHeader: function() {
      return getRoomDisplayName(this.room)
    }
  },
  props: {
    room: Object,
  }
}
</script>
