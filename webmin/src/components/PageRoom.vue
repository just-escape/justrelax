<template>
  <AppContent v-if="!room">
    <AppContentTitle slot="header-left">
      Room not found
    </AppContentTitle>
    <div class="text-center font-italic" slot="main">
      No actions available
    </div>
  </AppContent>

  <AppContent v-else>
    <div class="d-flex flex-row" slot="header-left">
      <AppContentTitle class="mr-5">
        {{ title }}
      </AppContentTitle>
      <RoomStartStop :roomId="room.id" class="my-auto"/>
    </div>
    <div class="d-flex flex-row" slot="header-right">
      <TicksClock :ticks="room.liveData.ticks" :displayZero="false" class="size-25 big-noodle mr-3"/>
      <AppNotificationButton class="my-auto"/>
    </div>

    <div slot="main">
      <PageRoomCameras :room="room" class="mb-4"/>
      <PageRoomTimeline :room="room" class="mb-4"/>
      <PageRoomActions :room="room"/>
    </div>
  </AppContent>
</template>

<script>
import AppContent from '@/components/AppContent.vue'
import AppContentTitle from '@/components/AppContentTitle.vue'
import AppNotificationButton from '@/components/AppNotificationButton.vue'
import TicksClock from '@/components/TicksClock.vue'
import RoomStartStop from '@/components/RoomStartStop.vue'
import PageRoomCameras from '@/components/PageRoomCameras.vue'
import PageRoomTimeline from '@/components/PageRoomTimeline.vue'
import PageRoomActions from '@/components/PageRoomActions.vue'
import roomStore from '@/store/roomStore.js'

export default {
  name: 'PageRoom',
  components: {
    AppContent,
    AppContentTitle,
    AppNotificationButton,
    TicksClock,
    RoomStartStop,
    PageRoomCameras,
    PageRoomTimeline,
    PageRoomActions,
  },
  computed: {
    room() {
      var room_id = parseInt(this.room_id, 10)
      if (Number.isNaN(room_id)) {
        return null
      }

      if (roomStore.state.rooms && roomStore.state.rooms[room_id] != undefined) {
        return roomStore.state.rooms[room_id]
      } else {
        return null
      }
    },
    title() {
      var title = this.room.scenario

      if (this.room.cardinal) {
        title = title + " - " + this.room.cardinal
      }

      return title
    }
  },
  props: ['room_id']
}
</script>
