<template>
  <div>
    <LightMonitorUnit
      class="monitor-unit"
      color="pink"
      :on="pinkSensor"
      :positionX="140 - 80 / 2"
      :positionY="0 + 135 - 80 / 2"
    />
    <LightMonitorUnit
      class="monitor-unit"
      color="yellow"
      :on="yellowSensor"
      :positionX="210 - 80 / 2"
      :positionY="40 + 135 - 80 / 2"
    />
    <LightMonitorUnit
      class="monitor-unit"
      color="green"
      :on="greenSensor"
      :positionX="210 - 80 / 2"
      :positionY="120 + 135 - 80 / 2"
    />
    <LightMonitorUnit
      class="monitor-unit"
      color="blue"
      :on="blueSensor"
      :positionX="140 - 80 / 2"
      :positionY="160 + 135 - 80 / 2"
    />
    <LightMonitorUnit
      class="monitor-unit"
      color="orange"
      :on="orangeSensor"
      :positionX="70 - 80 / 2"
      :positionY="120 + 135 - 80 / 2"
    />
    <LightMonitorUnit
      class="monitor-unit"
      color="purple"
      :on="true"
      :positionX="70 - 80 / 2"
      :positionY="40 + 135 - 80 / 2"
    />
  </div>
</template>

<script>
import LightMonitorUnit from '@/components/LightMonitorUnit.vue'
import lightStore from '@/store/lightStore.js'

export default {
  name: 'LightPuzzleMenuContent',
  components: {
    LightMonitorUnit,
  },
  computed: {
    yellowSensor: function() {
      return lightStore.state.sensors.yellow
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
    purpleSensor: function() {
      return lightStore.state.sensors.purple
    },
  }
}
</script>

<style scoped>
.monitor-unit {
  width: 80px;
}
</style>