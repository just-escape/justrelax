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
                  icon: "fa-fw fas fa-bullseye",
                },
                {
                  id: "c1r1b2",
                  icon: "fa-fw fas fa-bullseye",
                },
                {
                  id: "c1r1b3",
                  icon: "fa-fw fas fa-bullseye",
                },
                {
                  id: "c1r1b4",
                  icon: "fa-fw fas fa-bullseye",
                },
              ],
            },
            {
              name: "Row 2",
              buttons: [
                {
                  id: "c1r2b1",
                  icon: "fa-fw fas fa-bullseye",
                },
                {
                  id: "c1r2b2",
                  icon: "fa-fw fas fa-bullseye",
                },
                {
                  id: "c1r2b3",
                  icon: "fa-fw fas fa-bullseye",
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
                  icon: "fa-fw fas fa-bullseye",
                },
                {
                  id: "c1r3b3",
                  icon: "fa-fw fas fa-bullseye",
                },
                {
                  id: "c1r3b4",
                  icon: "fa-fw fas fa-bullseye",
                },
                {
                  id: "c1r3b5",
                  icon: "fa-fw fas fa-bullseye",
                },
              ],
            },
          ],
        },
        {
          name: "Card 2",
          rows: [
            {
              name: "Row 1",
              buttons: [
                {
                  id: "c2r1b1",
                  icon: "fa-fw fas fa-bullseye",
                },
                {
                  id: "c2r1b2",
                  icon: "fa-fw fas fa-bullseye",
                },
              ],
            },
            {
              name: "Row 2",
              buttons: [
                {
                  id: "c2r2b1",
                  icon: "fa-fw fas fa-bullseye",
                },
                {
                  id: "c2r2b2",
                  icon: "fa-fw fas fa-bullseye",
                },
                {
                  id: "c2r2b3",
                  icon: "fa-fw fas fa-bullseye",
                },
              ],
            },
          ],
        },
        {
          name: "Autres",
          rows: [
            {
              name: "Table",
              buttons: [
                {
                  id: "table_up",
                  icon: "fa-fw fas fa-arrow-up",
                },
                {
                  id: "table_down",
                  icon: "fa-fw fas fa-arrow-down",
                },
                {
                  id: "table_stop",
                  icon: "fa-fw far fa-hand-paper",
                },
              ],
            },
          ],
        },
        {
          name: "Lumières",
          rows: [
            {
              name: "Reset écran de synchro",
              buttons: [
                {
                  id: "reset_synchronizer",
                  icon: "fa-fw fas fa-undo-alt",
                },
              ],
            },
            {
              name: "Blanc",
              buttons: [
                {
                  id: "lights_on_white",
                  icon: "fa-fw far fa-sun",
                },
                {
                  id: "lights_off_white",
                  icon: "fa-fw fas fa-power-off",
                },
              ],
            },
            {
              name: "Bleu",
              buttons: [
                {
                  id: "lights_on_blue",
                  icon: "fa-fw far fa-sun",
                },
                {
                  id: "lights_off_blue",
                  icon: "fa-fw fas fa-power-off",
                },
              ],
            },
            {
              name: "Orange",
              buttons: [
                {
                  id: "lights_on_orange",
                  icon: "fa-fw far fa-sun",
                },
                {
                  id: "lights_off_orange",
                  icon: "fa-fw fas fa-power-off",
                },
              ],
            },
            {
              name: "Vert",
              buttons: [
                {
                  id: "lights_on_green",
                  icon: "fa-fw far fa-sun",
                },
                {
                  id: "lights_off_green",
                  icon: "fa-fw fas fa-power-off",
                },
              ],
            },
            {
              name: "Rouge",
              buttons: [
                {
                  id: "lights_on_red",
                  icon: "fa-fw far fa-sun",
                },
                {
                  id: "lights_off_red",
                  icon: "fa-fw fas fa-power-off",
                },
              ],
            },
            {
              name: "Rose",
              buttons: [
                {
                  id: "lights_on_pink",
                  icon: "fa-fw far fa-sun",
                },
                {
                  id: "lights_off_pink",
                  icon: "fa-fw fas fa-power-off",
                },
              ],
            },
          ],
        },
        {
          name: "Ventilation",
          rows: [
            {
              name: "Status panel",
              buttons: [
                {
                  id: "set_ventilation_panel_status_inactive",
                  icon: "fa-fw fas fa-lock",
                },
                {
                  id: "set_ventilation_panel_status_playing",
                  icon: "fa-fw fas fa-gamepad",
                },
                {
                  id: "set_ventilation_panel_status_success",
                  icon: "fa-fw fas fa-check",
                },
              ],
            },
            {
              name: "Difficulté",
              buttons: [
                {
                  id: "set_ventilation_panel_difficulty_easy",
                  icon: "fa-fw fas fa-dice-one",
                },
                {
                  id: "set_ventilation_panel_difficulty_normal",
                  icon: "fa-fw fas fa-dice-two",
                },
                {
                  id: "set_ventilation_panel_difficulty_hard",
                  icon: "fa-fw fas fa-dice-three",
                },
              ],
            },
            {
              name: "Écran de commande",
              buttons: [
                {
                  id: "reset_orders",
                  icon: "fa-fw fas fa-undo-alt",
                },
                {
                  id: "stop_orders_overlay_video",
                  icon: "fa-fw fas fa-video-slash",
                },
              ],
            },
          ],
        },
        {
          name: "Sokoban",
          rows: [
            {
              name: "Reset",
              buttons: [
                {
                  id: "reset_inventory",
                  icon: "fa-fw fas fa-undo-alt",
                },
              ],
            },
            {
              name: "Difficulté",
              buttons: [
                {
                  id: "set_inventory_difficulty_easy",
                  icon: "fa-fw fas fa-dice-one",
                },
                {
                  id: "set_inventory_difficulty_normal",
                  icon: "fa-fw fas fa-dice-two",
                },
                {
                  id: "set_inventory_difficulty_hard",
                  icon: "fa-fw fas fa-dice-three",
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
