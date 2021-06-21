<template>
  <div class="position-relative">
    <svg class="position-absolute">
      <defs>
        <filter id="glowing-rectangle" x="-50" y="-50" width="150" height="150">
          <feGaussianBlur result="blurOut" in="offOut" stdDeviation="5" />
          <feBlend in="SourceGraphic" in2="blurOut" mode="normal" />
        </filter>
      </defs>
    </svg>

    <!-- The pink light monitor unit is virtual (not displayed). Its use is only to trigger on/off publications. -->
    <LightMonitorUnitRectangle class="position-absolute d-none" :longEdge="monitorUnitSizeM" :vertical="true" color="pink" :triggerOnOffPublications="true"/>

    <div v-if="mapVersion === 1" class="d-flex flex-column justify-content-center h-100" style="margin-right: 30px">
      <div class="d-flex flex-row justify-content-end">
        <LightMonitorUnitRectangle :longEdge="monitorUnitSizeM" :vertical="true" color="blue" :triggerOnOffPublications="true"/>
        <LightMonitorUnitRectangle :longEdge="monitorUnitSizeM" :vertical="true" color="green" :triggerOnOffPublications="true"/>
      </div>
      <div class="d-flex flex-row justify-content-end">
        <LightMonitorUnitRectangle :longEdge="monitorUnitSizeM" :vertical="true" color="blue" :triggerOnOffPublications="false"/>
        <LightMonitorUnitRectangle :longEdge="monitorUnitSizeM" :vertical="true" color="white" :triggerOnOffPublications="true"/>
        <LightMonitorUnitRectangle :longEdge="monitorUnitSizeM" :vertical="true" color="red" :triggerOnOffPublications="true"/>
        <LightMonitorUnitRectangle :longEdge="monitorUnitSizeM" :vertical="true" color="orange" :triggerOnOffPublications="true"/>
      </div>
      <div class="d-flex flex-row justify-content-end">
        <LightMonitorUnitRectangle :longEdge="monitorUnitSizeM" :vertical="true" color="orange" :triggerOnOffPublications="false"/>
        <LightMonitorUnitRectangle :longEdge="monitorUnitSizeM" :vertical="true" color="white" :triggerOnOffPublications="false"/>
      </div>
    </div>
    <div v-else-if="mapVersion === 2" class="d-flex flex-column justify-content-around h-100 py-5">
      <div class="d-flex flex-row justify-content-center">
        <LightMonitorUnitRectangle :longEdge="monitorUnitSizeS" :vertical="false" color="green" :triggerOnOffPublications="true"/>
      </div>
      <div class="d-flex flex-row justify-content-center">
        <LightMonitorUnitRectangle :longEdge="monitorUnitSizeS" :vertical="false" color="blue" :triggerOnOffPublications="true"/>
      </div>
      <div class="d-flex flex-row justify-content-center">
        <LightMonitorUnitRectangle :longEdge="monitorUnitSizeS" :vertical="false" color="red" :triggerOnOffPublications="true"/>
      </div>
      <div class="d-flex flex-row justify-content-around" style="transform: translateY(10px) rotate(10deg)">
        <LightMonitorUnitRectangle :longEdge="monitorUnitSizeS" :vertical="false" color="orange" :triggerOnOffPublications="true"/>
        <LightMonitorUnitRectangle :longEdge="monitorUnitSizeS" :vertical="false" color="white" :triggerOnOffPublications="true"/>
        <LightMonitorUnitRectangle :longEdge="monitorUnitSizeS" :vertical="false" color="white" :triggerOnOffPublications="false"/>
      </div>
    </div>

    <div v-if="controls" class="position-absolute" style="top: 0">
      <div class="d-flex flex-row">
      <div
        class="ml-3 mr-2"
        style="border-radius: 50%; height: 50px; width: 50px; background: rgb(0, 170, 255)"
        :style="{opacity: getControlOpacity('blue')}"
        @click="toggleControls('blue')"
      ></div>
      <div
        class="mx-2"
        style="border-radius: 50%; height: 50px; width: 50px; background: rgb(220, 53, 69)"
        :style="{opacity: getControlOpacity('red')}"
        @click="toggleControls('red')"
      ></div>
      <div
        class="mx-2"
        style="border-radius: 50%; height: 50px; width: 50px; background: rgb(40, 167, 69)"
        :style="{opacity: getControlOpacity('green')}"
        @click="toggleControls('green')"
      ></div>
      <div
        class="mx-2"
        style="border-radius: 50%; height: 50px; width: 50px; background: rgb(253, 126, 20)"
        :style="{opacity: getControlOpacity('orange')}"
        @click="toggleControls('orange')"
      ></div>
      <div
        class="mx-2"
        style="border-radius: 50%; height: 50px; width: 50px; background: white"
        :style="{opacity: getControlOpacity('white')}"
        @click="toggleControls('white')"
      ></div>
      </div>

      <div @click="setManualMode" v-if="!isRestaurantInManualMode">not in manual mode</div>
    </div>
  </div>
</template>

<script>
import LightMonitorUnitRectangle from '@/components/LightMonitorUnitRectangle.vue'
import lightStore from '@/store/lightStore.js'

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
    getControlOpacity() {
      return (color) => {
        return lightStore.state.activatedSensors[color] ? 1 : 0.5
      }
    },
    mapVersion() {
      let mapVersion = this.$route.query.light_map_version
      if (mapVersion && mapVersion == 2) {
        return 2
      } else {
        return 1
      }
    },
    controls() {
      let controls = this.$route.query.controls
      if (controls && controls == 1) {
        return true
      } else {
        return false
      }
    },
    isRestaurantInManualMode() {
      return lightStore.state.isRestaurantInManualMode
    },
  },
  methods: {
    toggleControls(color) {
      lightStore.dispatch('toggleColor', {color: color, activated: !lightStore.state.activatedSensors[color]})
    },
    setManualMode() {
      lightStore.commit('setRestaurantInManualMode')
    }
  },
}
</script>