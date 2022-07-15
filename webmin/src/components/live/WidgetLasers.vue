<template>
  <div class="d-flex flex-column min-width-100px">
    <div class="text-one-line-ellipsis mb-1">{{ row.name }}</div>
    <div v-for="(laser, laserIndex) in row.widget_params.map" :key="roomId + '-' + laserIndex" class="d-flex flex-row justify-content-between rows-striped px-2 mb-1">
      <div class="d-flex flex-row align-items-center">
        <div
          class="border mr-1 position-relative pointer"
          style="border-color: #ef8649 !important; height: 17px; width: 17px"
          @click="togglePermanentActivation(laser.node, laser.prefix, laser.index)"
        >
          <i v-if="!isLaserDeactivated(laser.prefix, laser.index)" class="position-absolute text-jaffa fa fa-xs fa-fw fa-check" style="bottom: 0; right: 0"></i>
        </div>
        <div :style="{'text-decoration': isLaserBroken(laser.prefix, laser.index) ? 'line-through' : 'inherit'}">{{ laser.label }}</div>
      </div>
      <div class="d-flex flex-row align-items-center" :style="{opacity: isLaserDeactivated(laser.prefix, laser.index) || isLaserBroken(laser.prefix, laser.index) ? 0.2 : 1}">
        <i v-if="laser.dynamic" class="fa fa-fw fa-stopwatch"></i>
        <i v-if="laser.wall" class="fa fa-fw fa-ban"></i>
        <i class="fa fa-fw fa-dice-one" :style="{opacity: laser.easy ? 1 : 0.2}"></i>
        <i class="fa fa-fw fa-dice-two" :style="{opacity: laser.normal ? 1 : 0.2}"></i>
        <i class="fa fa-fw fa-dice-three mr-2" :style="{opacity: laser.hard ? 1 : 0.2}"></i>
        <span class="badge badge-secondary badge-pill text-right" style="background-color: #cb4299; width: 35px;">{{ laserAlarmCounters(laser.prefix, laser.index) }}</span>
      </div>
    </div>
    <div class="d-flex flex-row justify-content-between mt-1 mb-2">
      <div>Échecs avant désactivation auto</div>
      <div>
        <i v-if="failuresToAutoDeactivateDesynchroWarning" class="fa-fw fa fa-exclamation-triangle mr-2 text-danger"></i>
        <b-button-group>
          <ButtonJaffa
            size="sm"
            :disabled="failuresToAutoDeactivate === undefined || failuresToAutoDeactivateMin === undefined || failuresToAutoDeactivateMin >= failuresToAutoDeactivate"
            @click="setFailuresToAutoDeactivate(failuresToAutoDeactivate - 1)"
          >
            <i class="fa-fw fa fa-minus"></i>
          </ButtonJaffa>
          <div
            style="border-top: 1px solid #f38d40; border-bottom: 1px solid #f38d40; line-height: 1"
            class="d-flex justify-content-center align-items-center px-2"
            :style="{'border-color': failuresToAutoDeactivate === undefined ? '#949497' : '#f38d40', opacity: failuresToAutoDeactivate === undefined ? 0.65 : 1}"
          >
            <div>{{ failuresToAutoDeactivate }}</div>
          </div>
          <ButtonJaffa
            size="sm"
            :disabled="failuresToAutoDeactivate === undefined || failuresToAutoDeactivateMax === undefined || failuresToAutoDeactivateMax <= failuresToAutoDeactivate"
            @click="setFailuresToAutoDeactivate(failuresToAutoDeactivate + 1)"
          >
            <i class="fa-fw fa fa-plus"></i>
          </ButtonJaffa>
        </b-button-group>
      </div>
    </div>
    <div class="d-flex flex-row justify-content-between mb-2">
      <div>Délais capteurs (ms)</div>
      <div>
        <i v-if="checkSensorsDelayDesynchroWarning" class="fa-fw fa fa-exclamation-triangle mr-2 text-danger"></i>
        <b-button-group>
          <ButtonJaffa
            size="sm"
            class="position-relative"
            :disabled="checkSensorsDelay === undefined || checkSensorsDelayMin >= checkSensorsDelay"
            @click="setCheckSensorsDelay(checkSensorsDelay - 1000)"
          >
            <i class="fa-fw fa fa-minus"></i>
            <div
              class="position-absolute"
              style="bottom: 0; right: 0; font-size: 8px"
            >1000</div>
          </ButtonJaffa>
          <ButtonJaffa
            size="sm"
            class="position-relative"
            :disabled="checkSensorsDelay === undefined || checkSensorsDelayMin >= checkSensorsDelay"
            @click="setCheckSensorsDelay(checkSensorsDelay - 100)"
          >
            <i class="fa-fw fa fa-minus"></i>
            <div
              class="position-absolute"
              style="bottom: 0; right: 0; font-size: 8px"
            >100</div>
          </ButtonJaffa>
          <div
            style="border-top: 1px solid #f38d40; border-bottom: 1px solid #f38d40; line-height: 1"
            class="d-flex justify-content-center align-items-center px-2"
            :style="{'border-color': checkSensorsDelay === undefined ? '#949497' : '#f38d40', opacity: checkSensorsDelay === undefined ? 0.65 : 1}"
          >
            <div>{{ checkSensorsDelay }}</div>
          </div>
          <ButtonJaffa
            size="sm"
            class="position-relative"
            :disabled="checkSensorsDelay === undefined || checkSensorsDelayMax <= checkSensorsDelay"
            @click="setCheckSensorsDelay(checkSensorsDelay + 100)"
          >
            <i class="fa-fw fa fa-plus"></i>
            <div
              class="position-absolute"
              style="bottom: 0; right: 0; font-size: 8px"
            >100</div>
          </ButtonJaffa>
          <ButtonJaffa
            size="sm"
            class="position-relative"
            :disabled="checkSensorsDelay === undefined || checkSensorsDelayMax <= checkSensorsDelay"
            @click="setCheckSensorsDelay(checkSensorsDelay + 1000)"
          >
            <i class="fa-fw fa fa-plus"></i>
            <div
              class="position-absolute"
              style="bottom: 0; right: 0; font-size: 8px"
            >1000</div>
          </ButtonJaffa>
        </b-button-group>
      </div>
    </div>
    <div class="d-flex flex-row justify-content-between mb-2">
      <div>Vitesse lasers dynamiques</div>
      <div>
        <i v-if="dynamicLasersDifficultyDesynchroWarning" class="fa-fw fa fa-exclamation-triangle mr-2 text-danger"></i>
        <b-button-group>
          <ButtonJaffa
            size="sm"
            :active="dynamicLasersDifficulty === 'easy'"
            @click="setDynamicLasersDifficulty('easy')"
          >
            <i class="fa-fw fa fa-dice-one"></i>
          </ButtonJaffa>
          <ButtonJaffa
            size="sm"
            :active="dynamicLasersDifficulty === 'normal'"
            @click="setDynamicLasersDifficulty('normal')"
          >
            <i class="fa-fw fa fa-dice-two"></i>
          </ButtonJaffa>
          <ButtonJaffa
            size="sm"
            :active="dynamicLasersDifficulty === 'hard'"
            @click="setDynamicLasersDifficulty('hard')"
          >
            <i class="fa-fw fa fa-dice-three"></i>
          </ButtonJaffa>
        </b-button-group>
      </div>
    </div>
    <div class="d-flex flex-row justify-content-between mb-2">
      <div>Autodétection des lasers cassés</div>
      <div>
          <ButtonJaffa
            size="sm"
            @click="autoControl"
          >
            <i class="fa-fw fa fa-balance-scale"></i>
          </ButtonJaffa>
      </div>
    </div>
  </div>
</template>

<script>
import ButtonJaffa from "@/components/common/ButtonJaffa.vue"
import roomStore from "@/store/roomStore.js"

export default {
  name: "WidgetLasers",
  components: {
    ButtonJaffa,
  },
  data() {
    return {
      checkSensorsDelayMin: 100,
      checkSensorsDelayMax: 10000,
    }
  },
  computed: {
    failuresToAutoDeactivateDesynchroWarning() {
      if (this.allFailuresToAutoDeactivateMin.length > 0 && !this.allFailuresToAutoDeactivateMin.every(x => x === this.allFailuresToAutoDeactivateMin[0])) {
        return true
      }

      if (this.allFailuresToAutoDeactivateMax.length > 0 && !this.allFailuresToAutoDeactivateMax.every(x => x === this.allFailuresToAutoDeactivateMax[0])) {
        return true
      }

      if (this.allFailuresToAutoDeactivate.length > 0 && !this.allFailuresToAutoDeactivate.every(x => x === this.allFailuresToAutoDeactivate[0])) {
        return true
      }

      return false
    },
    failuresToAutoDeactivateMin() {
      return this.allFailuresToAutoDeactivateMin[0]
    },
    allFailuresToAutoDeactivateMin() {
      return [
        roomStore.state.sessionData[this.roomId]['laser_failures_to_auto_deactivate_min_A'],
        roomStore.state.sessionData[this.roomId]['laser_failures_to_auto_deactivate_min_B'],
      ].filter(x => x !== undefined)
    },
    failuresToAutoDeactivateMax() {
      return this.allFailuresToAutoDeactivateMax[0]
    },
    allFailuresToAutoDeactivateMax() {
      return [
        roomStore.state.sessionData[this.roomId]['laser_failures_to_auto_deactivate_max_A'],
        roomStore.state.sessionData[this.roomId]['laser_failures_to_auto_deactivate_max_B'],
      ].filter(x => x !== undefined)
    },
    failuresToAutoDeactivate() {
      return this.allFailuresToAutoDeactivate[0]
    },
    allFailuresToAutoDeactivate() {
      return [
        roomStore.state.sessionData[this.roomId]['laser_failures_to_auto_deactivate_A'],
        roomStore.state.sessionData[this.roomId]['laser_failures_to_auto_deactivate_B'],
      ].filter(x => x !== undefined)
    },
    checkSensorsDelayDesynchroWarning() {
      return this.allCheckSensorsDelay.length > 0 && !this.allCheckSensorsDelay.every(x => x === this.allCheckSensorsDelay[0])
    },
    checkSensorsDelay() {
      return this.allCheckSensorsDelay[0] * 10
    },
    allCheckSensorsDelay() {
      return [
        roomStore.state.sessionData[this.roomId]['laser_check_sensors_delay_A'],
        roomStore.state.sessionData[this.roomId]['laser_check_sensors_delay_B'],
      ].filter(x => x !== undefined)
    },
    dynamicLasersDifficultyDesynchroWarning() {
      return this.allDynamicLasersDifficulty.length > 0 && !this.allDynamicLasersDifficulty.every(x => x === this.allDynamicLasersDifficulty[0])
    },
    dynamicLasersDifficulty() {
      return this.allDynamicLasersDifficulty[0]
    },
    allDynamicLasersDifficulty() {
      return [
        roomStore.state.sessionData[this.roomId]['laser_dynamic_difficulty_A'],
        roomStore.state.sessionData[this.roomId]['laser_dynamic_difficulty_B'],
      ].filter(x => x !== undefined)
    },
    isLaserDeactivated() {
      return (laserPrefix, laserIndex) => {
        if (roomStore.state.sessionData[this.roomId]['deactivated_lasers_' + laserPrefix]) {
            return roomStore.state.sessionData[this.roomId]['deactivated_lasers_' + laserPrefix].includes(laserIndex)
        } else {
            return false
        }
      }
    },
    isLaserBroken() {
      return (laserPrefix, laserIndex) => {
        if (roomStore.state.sessionData[this.roomId]['broken_lasers_' + laserPrefix]) {
            return roomStore.state.sessionData[this.roomId]['broken_lasers_' + laserPrefix].includes(laserIndex)
        } else {
            return false
        }
      }
    },
    laserAlarmCounters() {
      return (laserPrefix, laserIndex) => {
        if (roomStore.state.sessionData[this.roomId]['laser_alarm_counters_' + laserPrefix]) {
          let value = roomStore.state.sessionData[this.roomId]['laser_alarm_counters_' + laserPrefix][laserIndex] || 0
          return value > 999 ? 999 : value
        } else {
          return 0
        }
      }
    },
  },
  methods: {
    setFailuresToAutoDeactivate(newValue) {
      if (isNaN(newValue)) {
        return
      }

      roomStore.dispatch('widgetAction', {
        channel: this.defaultChannel,
        widgetId: 'lasers',
        widgetType: 'lasers',
        action: 'set_failures_to_auto_deactivate',
        n: newValue,
      })
    },
    setCheckSensorsDelay(newValue) {
      if (isNaN(newValue)) {
        return
      }

      let boundedNewValue = Math.max(this.checkSensorsDelayMin, Math.min(this.checkSensorsDelayMax, newValue)) / 10

      roomStore.dispatch('widgetAction', {
        channel: this.defaultChannel,
        widgetId: 'lasers',
        widgetType: 'lasers',
        action: 'set_check_sensors_delay',
        n: boundedNewValue,
      })
    },
    setDynamicLasersDifficulty(newValue) {
      roomStore.dispatch('widgetAction', {
        channel: this.defaultChannel,
        widgetId: 'lasers',
        widgetType: 'lasers',
        action: 'set_dynamic_lasers_difficulty',
        difficulty: newValue,
      })
    },
    autoControl() {
      roomStore.dispatch('widgetAction', {
        channel: this.defaultChannel,
        widgetId: 'lasers',
        widgetType: 'lasers',
        action: 'set_status',
        status: 'auto_control',
      })
    },
    togglePermanentActivation(nodeChannel, prefix, index) {
      roomStore.dispatch('widgetAction', {
        channel: this.defaultChannel,
        widgetId: 'lasers',
        widgetType: 'lasers',
        action: 'set_activated',
        activated: this.isLaserDeactivated(prefix, index),
        laser_maze_channel: nodeChannel,
        laser_index: index,
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

<style scoped>
.rows-striped:nth-child(odd) {
  background: #4d4d4f;
}
</style>