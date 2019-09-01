<template>
  <div>
    <h2 class="big-noodle text-jaffa text-center">Rooms</h2>
    <div class="row">
      <div
        v-for="room in rooms"
        :key="room.id"
        class="col-4"
      >
        <PageHomeRoomRud :room="room"/>
      </div>
      <div class="col-4">
        <PageHomeRoomCreate/>
      </div>
    </div>
  </div>
</template>

<script>
import roomStore from '@/store/roomStore.js'
import PageHomeRoomRud from '@/components/PageHomeRoomRud.vue'
import PageHomeRoomCreate from '@/components/PageHomeRoomCreate.vue'

export default {
  name: 'PageHomeRooms',
  components: {
    PageHomeRoomRud,
    PageHomeRoomCreate,
  },
  data: function() {
    return {
      rooms: roomStore.state.rooms
    }
  },
}
</script>
