<template>
  <div>
    <!-- The pink light monitor unit is virtual (not displayed). Its use is only to trigger on/off publications. -->
    <LightMonitorUnitRectangle class="position-absolute d-none" :longEdge="monitorUnitSizeM" :vertical="true" color="pink" :triggerOnOffPublications="true"/>

    <div v-if="mapVersion === 1" class="d-flex flex-column justify-content-center h-100" style="margin-right: 30px">
      <div class="d-flex flex-row justify-content-end">
        <LightMonitorUnitRectangle :longEdge="monitorUnitSizeM" :vertical="true" color="blue" :triggerOnOffPublications="true"/>
        <LightMonitorUnitRectangle :longEdge="monitorUnitSizeM" :vertical="true" color="green" :triggerOnOffPublications="true"/>
      </div>
      <div class="d-flex flex-row justify-content-end">
        <LightMonitorUnitRectangle :longEdge="monitorUnitSizeM" :vertical="true" color="blue" :triggerOnOffPublications="true"/>
        <LightMonitorUnitRectangle :longEdge="monitorUnitSizeM" :vertical="true" color="white" :triggerOnOffPublications="true"/>
        <LightMonitorUnitRectangle :longEdge="monitorUnitSizeM" :vertical="true" color="red" :triggerOnOffPublications="true"/>
        <LightMonitorUnitRectangle :longEdge="monitorUnitSizeM" :vertical="true" color="orange" :triggerOnOffPublications="true"/>
      </div>
      <div class="d-flex flex-row justify-content-end">
        <LightMonitorUnitRectangle :longEdge="monitorUnitSizeM" :vertical="true" color="orange" :triggerOnOffPublications="true"/>
        <LightMonitorUnitRectangle :longEdge="monitorUnitSizeM" :vertical="true" color="white" :triggerOnOffPublications="true"/>
      </div>
    </div>
    <div v-else-if="mapVersion === 2" class="d-flex flex-column justify-content-around h-100 py-5">
      <div class="d-flex flex-row justify-content-center">
        <LightMonitorUnitRectangle :longEdge="monitorUnitSizeS" :vertical="false" color="green"/>
      </div>
      <div class="d-flex flex-row justify-content-center">
        <LightMonitorUnitRectangle :longEdge="monitorUnitSizeS" :vertical="false" color="blue"/>
      </div>
      <div class="d-flex flex-row justify-content-center">
        <LightMonitorUnitRectangle :longEdge="monitorUnitSizeS" :vertical="false" color="red"/>
      </div>
      <div class="d-flex flex-row justify-content-around" style="transform: translateY(10px) rotate(10deg)">
        <LightMonitorUnitRectangle :longEdge="monitorUnitSizeS" :vertical="false" color="orange"/>
        <LightMonitorUnitRectangle :longEdge="monitorUnitSizeS" :vertical="false" color="white"/>
        <LightMonitorUnitRectangle :longEdge="monitorUnitSizeS" :vertical="false" color="white"/>
      </div>
    </div>
  </div>
</template>

<script>
import LightMonitorUnitRectangle from '@/components/LightMonitorUnitRectangle.vue'

export default {
  name: 'LightPuzzleMenuContent',
  components: {
    LightMonitorUnitRectangle,
  },
  data() {
    return {
      monitorUnitSizeM: 120,
      monitorUnitSizeS: 100,
    }
  },
  computed: {
    mapVersion() {
      let mapVersion = this.$route.query.light_map_version
      if (mapVersion && mapVersion == 2) {
        return 2
      } else {
        return 1
      }
    }
  },
}
</script>