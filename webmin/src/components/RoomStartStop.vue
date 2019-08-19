<template>
  <b-button-group>
    <ButtonJaffa @click="run()">
      <i class="fas fa-play"></i>
    </ButtonJaffa>
    <ButtonJaffa @click="halt()">
      <i class="fas fa-pause"></i>
    </ButtonJaffa>
    <ButtonJaffa @click="reset()">
      <i class="fas fa-undo-alt"></i>
    </ButtonJaffa>
  </b-button-group>
</template>

<script>
import ButtonJaffa from '@/components/ButtonJaffa.vue'
import roomStore from '@/store/roomStore.js'
import notificationStore from '@/store/notificationStore.js'

export default {
  name: 'RoomStartStop',
  components: {
    ButtonJaffa
  },
  methods: {
    run: function () {
      roomStore.dispatch('runRoom', this.channel)
      notificationStore.dispatch('displayNotification', 'Room started')
    },
    halt: function () {
      roomStore.dispatch('haltRoom', this.channel)
      notificationStore.dispatch('displayNotification', 'Room halted')
    },
    reset: function () {
      roomStore.dispatch('resetRoom', this.channel)
      notificationStore.dispatch('displayNotification', 'Room reset')
    }
  },
  props: ['channel']
}
</script>
