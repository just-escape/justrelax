<template>
  <div>
    <h2 class="big-noodle text-jaffa text-center">Rooms</h2>
    <div class="row">
      <div
        v-for="room in rooms"
        :key="room.id"
        class="col-4"
      >
        <RoomRead :room="room"/>
      </div>
    </div>
  </div>
</template>

<script>
import RoomRead from '@/components/home/RoomRead.vue'
import roomStore from '@/store/roomStore.js'

export default {
  name: 'Rooms',
  components: {
    RoomRead,
  },
  computed: {
    rooms() {
      return roomStore.state.rooms
    }
  },
}
</script>
