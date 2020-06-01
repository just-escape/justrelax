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
      :style="{width: monitorUnitSize + 'px'}"
      color="blue"
      :positionX="140 - monitorUnitSize / 2"
      :positionY="0 + 135 - monitorUnitSize / 2"
    />
    <LightMonitorUnit
      :style="{width: monitorUnitSize + 'px'}"
      color="white"
      :positionX="210 - monitorUnitSize / 2"
      :positionY="40 + 135 - monitorUnitSize / 2"
    />
    <LightMonitorUnit
      :style="{width: monitorUnitSize + 'px'}"
      color="pink"
      :positionX="210 - monitorUnitSize / 2"
      :positionY="120 + 135 - monitorUnitSize / 2"
    />
    <LightMonitorUnit
      :style="{width: monitorUnitSize + 'px'}"
      color="red"
      :positionX="140 - monitorUnitSize / 2"
      :positionY="160 + 135 - monitorUnitSize / 2"
    />
    <LightMonitorUnit
      :style="{width: monitorUnitSize + 'px'}"
      color="green"
      :positionX="70 - monitorUnitSize / 2"
      :positionY="120 + 135 - monitorUnitSize / 2"
    />
    <LightMonitorUnit
      :style="{width: monitorUnitSize + 'px'}"
      color="orange"
      :positionX="70 - monitorUnitSize / 2"
      :positionY="40 + 135 - monitorUnitSize / 2"
    />
  </div>
</template>

<script>
import LightMonitorUnit from '@/components/LightMonitorUnit.vue'
import LightMonitorConnector from '@/components/LightMonitorConnector.vue'

export default {
  name: 'LightPuzzleMenuContent',
  components: {
    LightMonitorUnit,
    LightMonitorConnector,
  },
  data() {
    return {
      monitorUnitSize: 150
    }
  }
}
</script>