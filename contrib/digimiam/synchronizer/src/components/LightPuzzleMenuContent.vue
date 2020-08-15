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
      :width="monitorUnitSize"
      color="blue"
      :positionX="185 - monitorUnitSize / 2"
      :positionY="40 + 135 - monitorUnitSize / 2"
      :trianglesPositionX="185 - monitorUnitSize / 2"
      :trianglesPositionY="40 + 135 - monitorUnitSize / 2"
      :trianglesRotation="'0deg'"
    />
    <LightMonitorUnit
      :width="monitorUnitSize"
      color="white"
      :positionX="255 - monitorUnitSize / 2"
      :positionY="80 + 135 - monitorUnitSize / 2"
      :trianglesPositionX="270 - monitorUnitSize / 2"
      :trianglesPositionY="80 + 143 - monitorUnitSize / 2"
      :trianglesRotation="'60deg'"
    />
    <LightMonitorUnit
      :width="monitorUnitSize"
      color="pink"
      :positionX="255 - monitorUnitSize / 2"
      :positionY="160 + 135 - monitorUnitSize / 2"
      :trianglesPositionX="270 - monitorUnitSize / 2"
      :trianglesPositionY="160 + 159 - monitorUnitSize / 2"
      :trianglesRotation="'120deg'"
    />
    <LightMonitorUnit
      :width="monitorUnitSize"
      color="red"
      :positionX="185 - monitorUnitSize / 2"
      :positionY="200 + 135 - monitorUnitSize / 2"
      :trianglesPositionX="185 - monitorUnitSize / 2"
      :trianglesPositionY="200 + 170 - monitorUnitSize / 2"
      :trianglesRotation="'180deg'"
    />
    <LightMonitorUnit
      :width="monitorUnitSize"
      color="green"
      :positionX="115 - monitorUnitSize / 2"
      :positionY="160 + 135 - monitorUnitSize / 2"
      :trianglesPositionX="102 - monitorUnitSize / 2"
      :trianglesPositionY="160 + 159 - monitorUnitSize / 2"
      :trianglesRotation="'240deg'"
    />
    <LightMonitorUnit
      :width="monitorUnitSize"
      color="orange"
      :positionX="115 - monitorUnitSize / 2"
      :positionY="80 + 135 - monitorUnitSize / 2"
      :trianglesPositionX="102 - monitorUnitSize / 2"
      :trianglesPositionY="80 + 145 - monitorUnitSize / 2"
      :trianglesRotation="'300deg'"
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