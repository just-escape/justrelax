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
      :on="pinkSensor"
      :positionX="140 - 80 / 2"
      :positionY="0 + 135 - 80 / 2"
    />
    <LightMonitorUnit
      class="monitor-unit"
      color="white"
      :on="yellowSensor"
      :positionX="210 - 80 / 2"
      :positionY="40 + 135 - 80 / 2"
    />
    <LightMonitorUnit
      class="monitor-unit"
      color="pink"
      :on="greenSensor"
      :positionX="210 - 80 / 2"
      :positionY="120 + 135 - 80 / 2"
    />
    <LightMonitorUnit
      class="monitor-unit"
      color="red"
      :on="blueSensor"
      :positionX="140 - 80 / 2"
      :positionY="160 + 135 - 80 / 2"
    />
    <LightMonitorUnit
      class="monitor-unit"
      color="green"
      :on="orangeSensor"
      :positionX="70 - 80 / 2"
      :positionY="120 + 135 - 80 / 2"
    />
    <LightMonitorUnit
      class="monitor-unit"
      color="orange"
      :on="true"
      :positionX="70 - 80 / 2"
      :positionY="40 + 135 - 80 / 2"
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
  width: 80px;
}
</style>