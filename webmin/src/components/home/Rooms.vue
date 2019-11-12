<template>
  <div>
    <h2 class="big-noodle text-jaffa text-center">Rooms</h2>
    <div class="row">
      <div
        v-for="room in rooms"
        :key="room.id"
        class="col-4"
      >
        <RoomRud :room="room"/>
      </div>
      <div class="col-4">
        <RoomCreate/>
      </div>
    </div>
  </div>
</template>

<script>
import RoomRud from '@/components/home/RoomRud.vue'
import RoomCreate from '@/components/home/RoomCreate.vue'
import roomStore from '@/store/roomStore.js'

export default {
  name: 'Rooms',
  components: {
    RoomRud,
    RoomCreate,
  },
  data: function() {
    return {
      rooms: roomStore.state.rooms
    }
  },
}
</script>
