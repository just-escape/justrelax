<template>
    <div class="d-flex justify-content-between align-items-center">
        <div class="text-one-line-ellipsis min-width-100px">
            {{ row.name }}
        </div>
        <div>
            <b-button-group v-if="timerData">
              <Clock
                class="border-jaffa"
                style="border-width: 1px; border-style: solid; border-top-left-radius: 0.2rem; border-bottom-left-radius: 0.2rem; line-height: 28px; padding-right: 3px; padding-left: 3px"
                :seconds="remainingTime"
                :displayZero="true"
              />
              <ButtonJaffa
                v-if="state == 'NOT_STARTED' || state == 'PAUSED'"
                size="sm"
                @click="start"
              >
                <i class="fa fa-fw fa-play"></i>
              </ButtonJaffa>
              <ButtonJaffa
                v-if="state == 'TICKING'"
                size="sm"
                @click="pause"
              >
                <i class="fa fa-fw fa-pause"></i>
              </ButtonJaffa>
              <ButtonJaffa
                v-if="state == 'PAUSED'"
                size="sm"
                @click="cancel"
              >
                <i class="fa fa-fw fa-undo-alt"></i>
              </ButtonJaffa>
              <ButtonJaffa
                size="sm"
                @click="execute"
                :title="row.widget_params.execute_help"
              >
                <i class="fa fa-fw fa-terminal"></i>
              </ButtonJaffa>
            </b-button-group>
        </div>
    </div>
</template>

<script>
import roomStore from "@/store/roomStore.js"
import Clock from "@/components/common/Clock.vue"
import ButtonJaffa from "@/components/common/ButtonJaffa.vue"

export default {
  name: "WidgetTimer",
  components: {
    Clock,
    ButtonJaffa,
  },
  computed: {
    timerData() {
      return roomStore.state.sessionData[this.roomId][this.row.widget_params.name]
    },
    remainingTime() {
      return this.timerData.remaining_time
    },
    state() {
      return this.timerData.state
    },
    manuallyPaused() {
      return this.timerData.manually_paused
    },
    executed() {
      return this.timerData.executed
    },
    delay() {
      return this.timerData.delay
    },
  },
  methods: {
    start() {
      roomStore.dispatch('widgetAction', {
          channel: this.defaultChannel,
          widgetId: this.row.widget_params.name,
          widgetType: 'timer',
          action: 'start',
          name: this.row.widget_params.name,
      })
    },
    pause() {
      roomStore.dispatch('widgetAction', {
          channel: this.defaultChannel,
          widgetId: this.row.widget_params.name,
          widgetType: 'timer',
          action: 'pause',
          name: this.row.widget_params.name,
      })
    },
    cancel() {
      roomStore.dispatch('widgetAction', {
          channel: this.defaultChannel,
          widgetId: this.row.widget_params.name,
          widgetType: 'timer',
          action: 'cancel',
          name: this.row.widget_params.name,
      })
    },
    execute() {
      roomStore.dispatch('widgetAction', {
          channel: this.defaultChannel,
          widgetId: this.row.widget_params.name,
          widgetType: 'timer',
          action: 'execute',
          name: this.row.widget_params.name,
      })
    },
  },
  props: [
    "defaultChannel",
    "row",
    "roomId",
  ]
}
</script>