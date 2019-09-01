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
      <PageLiveCameras :room="room" class="mb-4"/>
      <PageLiveTimeline :room="room" class="mb-4"/>
      <PageLiveActions :room="room"/>
    </div>
  </AppContent>
</template>

<script>
import AppContent from '@/components/AppContent.vue'
import AppContentTitle from '@/components/AppContentTitle.vue'
import AppNotificationButton from '@/components/AppNotificationButton.vue'
import TicksClock from '@/components/TicksClock.vue'
import RoomStartStop from '@/components/RoomStartStop.vue'
import PageLiveCameras from '@/components/PageLiveCameras.vue'
import PageLiveTimeline from '@/components/PageLiveTimeline.vue'
import PageLiveActions from '@/components/PageLiveActions.vue'
import roomStore from '@/store/roomStore.js'

export default {
  name: 'PageLive',
  components: {
    AppContent,
    AppContentTitle,
    AppNotificationButton,
    TicksClock,
    RoomStartStop,
    PageLiveCameras,
    PageLiveTimeline,
    PageLiveActions,
  },
  computed: {
    room() {
      var roomId = parseInt(this.roomId, 10)
      if (Number.isNaN(roomId)) {
        return null
      }

      if (roomStore.state.rooms && roomStore.state.rooms[roomId] != undefined) {
        return roomStore.state.rooms[roomId]
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
  props: ['roomId']
}
</script>
