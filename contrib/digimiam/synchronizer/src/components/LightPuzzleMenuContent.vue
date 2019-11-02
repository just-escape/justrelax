<template>
  <div class="w-100 d-flex flex-column justify-content-between p-2">
    <div class="d-flex flex-column">
      <LightMonitorUnit
        class="monitor-unit d-inline-block"
        color="pink"
        :on="pinkSensor"
      />
      <LightMonitorUnit
        class="monitor-unit d-inline-block"
        color="yellow"
        :on="yellowSensor"
      />
      <LightMonitorUnit
        class="monitor-unit d-inline-block"
        color="green"
        :on="greenSensor"
      />
      <LightMonitorUnit
        class="monitor-unit d-inline-block"
        color="blue"
        :on="blueSensor"
      />
      <LightMonitorUnit
        class="monitor-unit d-inline-block"
        color="orange"
        :on="orangeSensor"
      />
      <LightMonitorUnit
        class="monitor-unit d-inline-block"
        color="purple"
        :on="purpleSensor"
      />
    </div>
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
  width: 40px;
}
</style>