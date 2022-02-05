<template>
  <div class="d-flex flex-column min-width-100px">
    <div class="text-one-line-ellipsis mb-1">{{ row.name }}</div>
    <div v-for="(laser, laserIndex) in row.widget_params" :key="roomId + '-' + laserIndex" class="d-flex flex-row justify-content-between rows-striped px-2">
      <div class="d-flex flex-row align-items-center">
        <div
          class="border mr-1 position-relative pointer"
          style="border-color: #ef8649 !important; height: 17px; width: 17px"
          @click="togglePermanentActivation(laser.node, laser.prefix, laser.index)"
        >
          <i v-if="!isLaserDeactivated(laser.prefix, laser.index)" class="position-absolute text-jaffa fa fa-xs fa-fw fa-check" style="bottom: 0; right: 0"></i>
        </div>
        <div>{{ laser.label }}</div>
      </div>
      <div class="d-flex flex-row align-items-center" :style="{opacity: isLaserDeactivated(laser.prefix, laser.index) ? 0.2 : 1}">
        <i v-if="laser.dynamic" class="fa fa-fw fa-stopwatch"></i>
        <i v-if="laser.wall" class="fa fa-fw fa-ban"></i>
        <i class="fa fa-fw fa-dice-one" :style="{opacity: laser.easy ? 1 : 0.2}"></i>
        <i class="fa fa-fw fa-dice-two" :style="{opacity: laser.normal ? 1 : 0.2}"></i>
        <i class="fa fa-fw fa-dice-three mr-2" :style="{opacity: laser.hard ? 1 : 0.2}"></i>
        <span class="badge badge-secondary badge-pill text-right" style="background-color: #cb4299; width: 35px;">{{ laserAlarmCounters(laser.prefix, laser.index) }}</span>
      </div>
    </div>
  </div>
</template>

<script>
import roomStore from "@/store/roomStore.js"

export default {
  name: "WidgetLasers",
  computed: {
    isLaserDeactivated() {
      return (laserPrefix, laserIndex) => {
        if (roomStore.state.sessionData[this.roomId]['deactivated_lasers_' + laserPrefix]) {
            return roomStore.state.sessionData[this.roomId]['deactivated_lasers_' + laserPrefix].includes(laserIndex)
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
    togglePermanentActivation(nodeChannel, prefix, index) {
      let action = this.isLaserDeactivated(prefix, index) ? "reactivate_permanently" : "deactivate_permanently"
      roomStore.dispatch('widgetAction', {
        channel: this.defaultChannel,
        widgetId: 'lasers',
        widgetType: 'lasers',
        action: action,
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