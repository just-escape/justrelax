<template>
  <b-button-group>
    <ButtonJaffa size="md" @click="action('run')">
      <i class="fas fa-play"></i>
    </ButtonJaffa>
    <ButtonJaffa size="md" @click="action('halt')">
      <i class="fas fa-pause"></i>
    </ButtonJaffa>
    <ButtonJaffa size="md" @click="action('reset')">
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
    action(actionName) {
      roomStore.dispatch('widgetAction', {channel: this.channel, widgetId: 'start_stop', widgetType: 'start_stop', action: actionName})
    },
  },
  props: ['channel']
}
</script>
