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
      <SessionTimeClock :sessionTime="room.liveData.sessionTime" :displayZero="false" class="size-25 big-noodle mr-3"/>
      <NotificationButton class="my-auto"/>
    </div>

    <div slot="main">
      <Cameras :room="room" class="mb-4"/>
      <Timeline :room="room" class="mb-4"/>
      <SendEvent :room="room" class="mb-4"/>
      <!--<Actions :room="room"/>-->
      <AdminButtons :buttonCards="buttonCards" :room="room"/>
    </div>
  </AppContent>
</template>

<script>
import AppContent from '@/components/common/AppContent.vue'
import AppContentTitle from '@/components/common/AppContentTitle.vue'
import NotificationButton from '@/components/notification/Button.vue'
import SessionTimeClock from '@/components/common/SessionTimeClock.vue'
import StartStop from '@/components/live/StartStop.vue'
import Cameras from '@/components/live/Cameras.vue'
import Timeline from '@/components/live/Timeline.vue'
import SendEvent from '@/components/live/SendEvent.vue'
import AdminButtons from '@/components/live/AdminButtons.vue'
// import Actions from '@/components/live/Actions.vue'
import roomStore from '@/store/roomStore.js'

export default {
  name: 'PageLive',
  components: {
    AppContent,
    AppContentTitle,
    NotificationButton,
    SessionTimeClock,
    StartStop,
    Cameras,
    Timeline,
    SendEvent,
    AdminButtons,
    // Actions,
  },
  data() {
    return {
      buttonCards: [
        {
          name: "Card 1",
          rows: [
            {
              name: "Row 1",
              buttons: [
                {
                  id: "c1r1b1",
                  icon: "fas fa-bullseye",
                },
                {
                  id: "c1r1b2",
                  icon: "fas fa-bullseye",
                },
                {
                  id: "c1r1b3",
                  icon: "fas fa-bullseye",
                },
                {
                  id: "c1r1b4",
                  icon: "fas fa-bullseye",
                },
              ],
            },
            {
              name: "Row 2",
              buttons: [
                {
                  id: "c1r2b1",
                  icon: "fas fa-bullseye",
                },
                {
                  id: "c1r2b2",
                  icon: "fas fa-bullseye",
                },
                {
                  id: "c1r2b3",
                  icon: "fas fa-bullseye",
                },
              ],
            },
            {
              name: "Row 3",
              buttons: [
                {
                  id: "c1r3b1",
                  icon: "fas fa-bullseye",
                },
                {
                  id: "c1r3b2",
                  icon: "fas fa-bullseye",
                },
                {
                  id: "c1r3b3",
                  icon: "fas fa-bullseye",
                },
                {
                  id: "c1r3b4",
                  icon: "fas fa-bullseye",
                },
                {
                  id: "c1r3b5",
                  icon: "fas fa-bullseye",
                },
              ],
            },
          ],
        },        {
          name: "Card 2",
          rows: [
            {
              name: "Row 1",
              buttons: [
                {
                  id: "c2r1b1",
                  icon: "fas fa-bullseye",
                },
                {
                  id: "c2r1b2",
                  icon: "fas fa-bullseye",
                },
              ],
            },
            {
              name: "Row 2",
              buttons: [
                {
                  id: "c2r2b1",
                  icon: "fas fa-bullseye",
                },
                {
                  id: "c2r2b2",
                  icon: "fas fa-bullseye",
                },
                {
                  id: "c2r2b3",
                  icon: "fas fa-bullseye",
                },
              ],
            },
          ],
        },
      ],
    }
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
