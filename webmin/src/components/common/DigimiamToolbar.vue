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

        <div class="d-flex align-items-center">
          <div class="mr-2">
            Intro Mme Poivre
          </div>
          <div
            v-if="getData('ms_pepper_intro') !== undefined"
            class="border mr-1 position-relative pointer"
            style="border-color: #ef8649 !important; height: 17px; width: 17px"
            @click="setData('ms_pepper_intro', !getData('ms_pepper_intro'))"
          >
            <i v-if="getData('ms_pepper_intro')" class="position-absolute text-jaffa fa fa-xs fa-fw fa-check" style="bottom: 0; right: 0"></i>
          </div>
        </div>
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
    getData() {
      return (key) => roomStore.state.sessionData[this.roomId][key]
    },
  },
  methods: {
    action(actionName) {
      roomStore.dispatch('widgetAction', {channel: this.defaultPublicationChannel, widgetId: 'start_stop', widgetType: 'start_stop', action: actionName})
    },
    setData(key, value) {
      roomStore.dispatch('widgetAction', {
        channel: this.defaultPublicationChannel,
        widgetId: key,
        widgetType: 'session_data',
        action: 'set',
        key: key,
        value: value,
      })
    },
  },
  props: ['roomId', 'name', 'defaultPublicationChannel', "url"]
}
</script>
