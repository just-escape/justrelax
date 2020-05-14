<template>
  <div>
    <LightMonitorConnector
      :x1="210"
      :y1="40 + 135"
      :x2="210"
      :y2="120 + 135"
      :thickness="10"
    />
    <LightMonitorConnector
      :x1="140"
      :y1="160 + 135"
      :x2="210"
      :y2="120 + 135"
      :thickness="10"
    />

    <LightMonitorUnit
      class="monitor-unit"
      color="blue"
      :on="blueSensor"
      :positionX="140 - 90 / 2"
      :positionY="0 + 135 - 90 / 2"
    />
    <LightMonitorUnit
      class="monitor-unit"
      color="white"
      :on="whiteSensor"
      :positionX="210 - 90 / 2"
      :positionY="40 + 135 - 90 / 2"
    />
    <LightMonitorUnit
      class="monitor-unit"
      color="pink"
      :on="pinkSensor"
      :positionX="210 - 90 / 2"
      :positionY="120 + 135 - 90 / 2"
    />
    <LightMonitorUnit
      class="monitor-unit"
      color="red"
      :on="redSensor"
      :positionX="140 - 90 / 2"
      :positionY="160 + 135 - 90 / 2"
    />
    <LightMonitorUnit
      class="monitor-unit"
      color="green"
      :on="greenSensor"
      :positionX="70 - 90 / 2"
      :positionY="120 + 135 - 90 / 2"
    />
    <LightMonitorUnit
      class="monitor-unit"
      color="orange"
      :on="orangeSensor"
      :positionX="70 - 90 / 2"
      :positionY="40 + 135 - 90 / 2"
    />
  </div>
</template>

<script>
import LightMonitorUnit from '@/components/LightMonitorUnit.vue'
import LightMonitorConnector from '@/components/LightMonitorConnector.vue'
import lightStore from '@/store/lightStore.js'

export default {
  name: 'LightPuzzleMenuContent',
  components: {
    LightMonitorUnit,
    LightMonitorConnector,
  },
  computed: {
    whiteSensor: function() {
      return lightStore.state.sensors.white
    },
    pinkSensor: function() {
      return lightStore.state.sensors.pink
    },
    orangeSensor: function() {
      return lightStore.state.sensors.orange
    },
    greenSensor: function() {
      return lightStore.state.sensors.green
    },
    blueSensor: function() {
      return lightStore.state.sensors.blue
    },
    redSensor: function() {
      return lightStore.state.sensors.red
    },
  }
}
</script>

<style scoped>
.monitor-unit {
  width: 90px;
}
</style>