<template>
  <div class="d-flex flex-row justify-content-between align-items-center">
    <div class="d-flex flex-row align-items-center">
        <div class="big-noodle mr-4" style="font-size: 22px; width: 140px">
          <a :href="url">{{ name }}</a>
        </div>

        <b-button-group class="mr-3">
          <ButtonJaffa size="md" @click="action('run')">
            <i class="fas fa-play"></i>
          </ButtonJaffa>
          <ButtonJaffa size="md" @click="action('halt')">
            <i class="fas fa-pause"></i>
          </ButtonJaffa>
          <ButtonJaffa size="md" @click="action('reset')">
            <i class="fas fa-undo-alt"></i>
          </ButtonJaffa>
          <ButtonJaffa class="position-relative" size="md" @click="action('start_tidy')">
            <i class="fas fa-random"></i>
            <i
              class="fa-fw fas fa-dice-one position-absolute"
              style="scale: 0.7; bottom: 0; right: 0"
            ></i>
          </ButtonJaffa>
          <ButtonJaffa class="position-relative" size="md" @click="action('end_tidy')">
            <i class="fas fa-random"></i>
            <i
              class="fa-fw fas fa-dice-two position-absolute"
              style="scale: 0.7; bottom: 0; right: 0"
            ></i>
          </ButtonJaffa>
        </b-button-group>
    </div>
    <div class="d-flex flex-row">
        <Clock :seconds="gameTime" :displayZero="true" class="big-noodle" style="font-size: 22px"/>
    </div>
  </div>
</template>

<script>
import ButtonJaffa from "@/components/common/ButtonJaffa.vue"
import Clock from "@/components/common/Clock.vue"
import roomStore from '@/store/roomStore.js'

export default {
  name: 'DigimiamToolbar',
  components: {
    ButtonJaffa,
    Clock,
  },
  computed: {
    gameTime() {
      return roomStore.state.sessionData[this.roomId].game_time
    },
  },
  methods: {
    action(actionName) {
      roomStore.dispatch('widgetAction', {channel: this.defaultPublicationChannel, widgetId: 'start_stop', widgetType: 'start_stop', action: actionName})
    },
  },
  props: ['roomId', 'name', 'defaultPublicationChannel', "url"]
}
</script>
