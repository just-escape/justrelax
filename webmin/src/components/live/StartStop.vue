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
import ButtonJaffa from '@/components/common/ButtonJaffa.vue'
import roomStore from '@/store/roomStore.js'

export default {
  name: 'StartStop',
  components: {
    ButtonJaffa
  },
  methods: {
    run: function () {
      roomStore.dispatch('runRoom', this.roomId)
    },
    halt: function () {
      roomStore.dispatch('haltRoom', this.roomId)
    },
    reset: function () {
      roomStore.dispatch('resetRoom', this.roomId)
    }
  },
  props: ['roomId']
}
</script>
