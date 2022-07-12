<template>
  <div class="d-flex flex-row justify-content-between align-items-center">
    <div class="d-flex flex-row align-items-center">
      <div class="big-noodle mr-4" style="font-size: 22px; width: 140px">
          <a :href="url">{{ name }}</a>
      </div>
      <b-button-group>
        <ButtonJaffa size="md" @click="powerOff">
          <i class="fas fa-power-off"></i>
        </ButtonJaffa>
        <ButtonJaffa size="md" @click="unlock">
          <i class="fas fa-unlock"></i>
        </ButtonJaffa>
        <ButtonJaffa
          size="md"
          @click="toggleMaintenance"
          :active="isInMaintenanceMode"
        >
          <i class="fas fa-tools"></i>
        </ButtonJaffa>
      </b-button-group>
    </div>
  </div>
</template>

<script>
import ButtonJaffa from "@/components/common/ButtonJaffa.vue"
import roomStore from '@/store/roomStore.js'
import preferenceStore from '@/store/preferenceStore.js'

export default {
  name: 'LinkToolbar',
  components: {
    ButtonJaffa,
  },
  computed: {
    isInMaintenanceMode() {
      return preferenceStore.state.isInMaintenanceMode
    },
  },
  methods: {
    toggleMaintenance() {
      preferenceStore.commit('setMaintenanceMode', !preferenceStore.state.isInMaintenanceMode)
    },
    powerOff() {
      roomStore.dispatch('widgetAction', {
        channel: 'd1.broadcast',
        widgetId: 'd1_poweroff',
        widgetType: 'd1_poweroff',
        action: 'click',
        category: "shutdown",
      })
      roomStore.dispatch('widgetAction', {
        channel: 'd2.broadcast',
        widgetId: 'd2_poweroff',
        widgetType: 'd2_poweroff',
        action: 'click',
        category: "shutdown",
      })
    },
    unlock() {
      roomStore.dispatch('widgetAction', {
        channel: 'justescape.player_lockers',
        widgetId: 'player_lockers_open',
        widgetType: 'player_lockers_open',
        action: 'justescape.player_lockers',
        category: "unlock_from_bitmask",
        bitmask: 63,
      })
    },
  },
  props: ['url', 'name']
}
</script>
