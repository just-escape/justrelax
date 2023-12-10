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

    <div v-if="mapVersion === 1" class="d-flex flex-column justify-content-center h-100" style="margin-right: 30px">
      <div class="d-flex flex-row justify-content-end">
        <LightMonitorUnitRectangle :longEdge="monitorUnitSizeM" :vertical="true" color="white" :colorId="6"/>
        <LightMonitorUnitRectangle :longEdge="monitorUnitSizeM" :vertical="true" color="red" :colorId="26"/>
      </div>
      <div class="d-flex flex-row justify-content-end">
        <LightMonitorUnitRectangle :longEdge="monitorUnitSizeM" :vertical="true" color="blue" :colorId="12"/>
        <LightMonitorUnitRectangle :longEdge="monitorUnitSizeM" :vertical="true" color="white" :colorId="16"/>
        <LightMonitorUnitRectangle :longEdge="monitorUnitSizeM" :vertical="true" color="blue" :colorId="21"/>
        <LightMonitorUnitRectangle :longEdge="monitorUnitSizeM" :vertical="true" color="orange" :colorId="19"/>
      </div>
      <div class="d-flex flex-row justify-content-end">
        <LightMonitorUnitRectangle :longEdge="monitorUnitSizeM" :vertical="true" color="orange" :colorId="20"/>
        <LightMonitorUnitRectangle :longEdge="monitorUnitSizeM" :vertical="true" color="green" :colorId="13"/>
      </div>
    </div>
    <div v-else-if="mapVersion === 2" class="d-flex flex-column justify-content-around h-100 py-5">
      <div class="d-flex flex-row justify-content-center">
        <LightMonitorUnitRectangle :longEdge="monitorUnitSizeS" :vertical="false" color="white" :colorId="5"/>
      </div>
      <div class="d-flex flex-row justify-content-center">
        <LightMonitorUnitRectangle :longEdge="monitorUnitSizeS" :vertical="false" color="blue" :colorId="0"/>
      </div>
      <div class="d-flex flex-row justify-content-center">
        <LightMonitorUnitRectangle :longEdge="monitorUnitSizeS" :vertical="false" color="green" :colorId="19"/>
      </div>
      <div class="d-flex flex-row justify-content-around" style="transform: translateY(10px) rotate(10deg)">
        <LightMonitorUnitRectangle :longEdge="monitorUnitSizeS" :vertical="false" color="white" :colorId="26"/>
        <LightMonitorUnitRectangle :longEdge="monitorUnitSizeS" :vertical="false" color="orange" :colorId="20"/>
        <LightMonitorUnitRectangle :longEdge="monitorUnitSizeS" :vertical="false" color="red" :colorId="21"/>
      </div>
    </div>

    <div v-if="controls" class="position-absolute" style="top: 0; z-index: 10">
      <div v-if="mapVersion === 1" class="d-flex flex-row">
        <div
          class="mx-2"
          style="border-radius: 50%; height: 50px; width: 50px; background: white"
          :style="{opacity: getControlOpacity('white', 6)}"
          @click="toggleControls('white', 6)"
        ></div>
        <div
          class="mx-2"
          style="border-radius: 50%; height: 50px; width: 50px; background: rgb(220, 53, 69)"
          :style="{opacity: getControlOpacity('red', 26)}"
          @click="toggleControls('red', 26)"
        ></div>
        <div
          class="mx-2"
          style="border-radius: 50%; height: 50px; width: 50px; background: rgb(0, 170, 255)"
          :style="{opacity: getControlOpacity('blue', 12)}"
          @click="toggleControls('blue', 12)"
        ></div>
        <div
          class="mx-2"
          style="border-radius: 50%; height: 50px; width: 50px; background: white"
          :style="{opacity: getControlOpacity('white', 16)}"
          @click="toggleControls('white', 16)"
        ></div>
        <div
          class="mx-2"
          style="border-radius: 50%; height: 50px; width: 50px; background: rgb(0, 170, 255)"
          :style="{opacity: getControlOpacity('blue', 21)}"
          @click="toggleControls('blue', 21)"
        ></div>
        <div
          class="mx-2"
          style="border-radius: 50%; height: 50px; width: 50px; background: rgb(253, 126, 20)"
          :style="{opacity: getControlOpacity('orange', 19)}"
          @click="toggleControls('orange', 19)"
        ></div>
        <div
          class="mx-2"
          style="border-radius: 50%; height: 50px; width: 50px; background: rgb(253, 126, 20)"
          :style="{opacity: getControlOpacity('orange', 20)}"
          @click="toggleControls('orange', 20)"
        ></div>
        <div
          class="mx-2"
          style="border-radius: 50%; height: 50px; width: 50px; background: rgb(40, 167, 69)"
          :style="{opacity: getControlOpacity('green', 13)}"
          @click="toggleControls('green', 13)"
        ></div>
      </div>
      <div v-else-if="mapVersion === 2" class="d-flex flex-row">
        <div
          class="ml-3 mr-2"
          style="border-radius: 50%; height: 50px; width: 50px; background: rgb(0, 170, 255)"
          :style="{opacity: getControlOpacity('blue', 0)}"
          @click="toggleControls('blue', 0)"
        ></div>
        <div
          class="mx-2"
          style="border-radius: 50%; height: 50px; width: 50px; background: rgb(220, 53, 69)"
          :style="{opacity: getControlOpacity('red', 5)}"
          @click="toggleControls('red', 5)"
        ></div>
        <div
          class="mx-2"
          style="border-radius: 50%; height: 50px; width: 50px; background: rgb(40, 167, 69)"
          :style="{opacity: getControlOpacity('green', 19)}"
          @click="toggleControls('green', 19)"
        ></div>
        <div
          class="mx-2"
          style="border-radius: 50%; height: 50px; width: 50px; background: white"
          :style="{opacity: getControlOpacity('white', 26)}"
          @click="toggleControls('white', 26)"
        ></div>
        <div
          class="mx-2"
          style="border-radius: 50%; height: 50px; width: 50px; background: rgb(253, 126, 20)"
          :style="{opacity: getControlOpacity('orange', 20)}"
          @click="toggleControls('orange', 20)"
        ></div>
        <div
          class="mx-2"
          style="border-radius: 50%; height: 50px; width: 50px; background: white"
          :style="{opacity: getControlOpacity('white', 21)}"
          @click="toggleControls('white', 21)"
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
      return (color, id) => {
        return lightStore.state.activatedSensors[color] && lightStore.state.activatedSensorIds[id] ? 1 : 0.5
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
    toggleControls(color, id) {
      lightStore.dispatch('toggleColor', {color: color, id: id, activated: !lightStore.state.activatedSensorIds[id]})
    },
    setManualMode() {
      lightStore.commit('setRestaurantInManualMode')
    }
  },
}
</script>