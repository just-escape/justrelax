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
      <StartStop :roomId="room.id" class="my-auto"/>
    </div>
    <div class="d-flex flex-row" slot="header-right">
      <TicksClock :ticks="room.liveData.ticks" :displayZero="false" class="size-25 big-noodle mr-3"/>
      <NotificationButton class="my-auto"/>
    </div>

    <div slot="main">
      <Cameras :room="room" class="mb-4"/>
      <Timeline :room="room" class="mb-4"/>
      <SendMessage :room="room" class="mb-4"/>
      <!--<Actions :room="room"/>-->
    </div>
  </AppContent>
</template>

<script>
import AppContent from '@/components/common/AppContent.vue'
import AppContentTitle from '@/components/common/AppContentTitle.vue'
import NotificationButton from '@/components/notification/Button.vue'
import TicksClock from '@/components/common/TicksClock.vue'
import StartStop from '@/components/live/StartStop.vue'
import Cameras from '@/components/live/Cameras.vue'
import Timeline from '@/components/live/Timeline.vue'
import SendMessage from '@/components/live/SendMessage.vue'
// import Actions from '@/components/live/Actions.vue'
import roomStore from '@/store/roomStore.js'

export default {
  name: 'PageLive',
  components: {
    AppContent,
    AppContentTitle,
    NotificationButton,
    TicksClock,
    StartStop,
    Cameras,
    Timeline,
    SendMessage,
    // Actions,
  },
  computed: {
    room() {
      return roomStore.getters.room(this.roomId)
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
