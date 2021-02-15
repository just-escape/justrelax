<template>
  <AppContent v-if="room === undefined">
    <AppContentTitle slot="header-left">
      {{ 'Loading...' }}
    </AppContentTitle>
    <div class="text-center font-italic" slot="main">
      {{ 'Loading...' }}
    </div>
  </AppContent>

  <AppContent v-else-if="room === null">
    <AppContentTitle slot="header-left">
      {{ 'Room not found' }}
    </AppContentTitle>
    <div class="text-center font-italic" slot="main">
      {{ 'No actions available' }}
    </div>
  </AppContent>

  <AppContent v-else>
    <div class="d-flex flex-row" slot="header-left">
      <AppContentTitle class="mr-5">
        {{ room.name }}
      </AppContentTitle>
      <StartStop :channel="room.default_publication_channel" class="my-auto"/>
    </div>
    <div class="d-flex flex-row" slot="header-right">
      <Clock :roomId="room.id" :data="'game_time'" :displayZero="true" class="size-25 big-noodle mr-3"/>
      <NotificationButton class="my-auto"/>
    </div>

    <div slot="main">
      <Cameras :roomId="room.id" class="mb-4"/>
      <!--<Timeline :room="room" class="mb-4"/>-->
      <PublishEvent :defaultChannel="room.default_publication_channel" class="mb-4"/>
      <Actions :roomId="room.id"/>
    </div>
  </AppContent>
</template>

<script>
import AppContent from '@/components/common/AppContent.vue'
import AppContentTitle from '@/components/common/AppContentTitle.vue'
import NotificationButton from '@/components/notification/Button.vue'
import Clock from '@/components/common/Clock.vue'
import StartStop from '@/components/live/StartStop.vue'
import Cameras from '@/components/live/Cameras.vue'
// import Timeline from '@/components/live/Timeline.vue'
import PublishEvent from '@/components/live/PublishEvent.vue'
import Actions from '@/components/live/Actions.vue'
import roomStore from '@/store/roomStore.js'

export default {
  name: 'PageLive',
  components: {
    AppContent,
    AppContentTitle,
    NotificationButton,
    Clock,
    StartStop,
    Cameras,
    // Timeline,
    PublishEvent,
    Actions,
  },
  computed: {
    room() {
      if (roomStore.state.rooms === undefined) {
        return undefined
      }

      var parsedRoomId = parseInt(this.roomId, 10)
      if (Number.isNaN(parsedRoomId)) {
        return null
      }

      for (var room of roomStore.state.rooms) {
        if (room.id === parsedRoomId) {
          return room
        }
      }

      return null
    },
  },
  props: ['roomId']
}
</script>
