<template>
  <div
    class="glowing-container h-100 d-flex flex-column justify-content-between overflow-hidden position-relative"
  >
    <div class="overflow-hidden position-relative">
      <div v-if="!lightSuccess && displayLightExplicitInstruction">
        <div
          class="position-absolute text-center pulse-opacity"
          style="z-index: 1; margin-top: 10px; left: 10px; width: 768px; background: rgba(255, 69, 0, 0.65)"
          :class="{'p-1': !isColorActivated || areTooManyLightsActivated}"
        >
          <div v-if="!isColorActivated">
            La lumière {{ colorIdToLocale[units[0].color] }} n'est pas allumée
          </div>
          <div v-else-if="areTooManyLightsActivated">
            Plusieurs lumières sont allumées en même temps : synchronisation ralentie
          </div>
        </div>
      </div>
      <transition-group name="sequence" tag="div" style="height: 394px; width: 1576px">
        <LightContainerUnit
          v-for="u in units"
          :key="u.id" :color="u.color"
          style="height: 330px; width: 330px; margin-left: 229px; margin-right: 229px"
          class="sequence-item d-inline-block"
          :id="u.id" :completeness="u.completeness" :activable="u.activable"
        />
      </transition-group>
    </div>
    <LightProgressionBar class="px-4 mb-4"/>
  </div>
</template>

<script>
import LightContainerUnit from '@/components/LightContainerUnit.vue'
import LightProgressionBar from '@/components/LightProgressionBar.vue'
import lightStore from '@/store/lightStore.js'

export default {
  name: 'LightContainer',
  components: {
    LightContainerUnit,
    LightProgressionBar,
  },
  data() {
    return {
      colorIdToLocale: {
        'blue': 'bleue',
        'orange': 'orange',
        'green': 'verte',
        'pink': 'rose',
        'red': 'rouge',
        'white': 'blanche',
      }
    }
  },
  computed: {
    displayLightExplicitInstruction() {
      return lightStore.state.displayLightExplicitInstruction
    },
    areTooManyLightsActivated() {
      if (!lightStore.state.strictLoadingMode) {
        return false
      }

      let counter = 0
      for (let k in lightStore.state.activatedSensors) {
        if (lightStore.state.activatedSensors[k]) {
          counter += 1
        }
      }

      if (this.units[0].color === 'pink') {
        if (counter > 3) {
          return true
        }
      } else {
        if (counter > 1) {
          return true
        }
      }
      return false
    },
    isColorActivated() {
      return lightStore.state.activatedSensors[this.units[0].color]
    },
    lightSuccess() {
      return lightStore.state.success
    },
    units() {
      return lightStore.state.sequence
    },
  },
}
</script>

<style scoped>
.sequence-item {
  transition: all 0.7s linear;
}

.sequence-enter {
  transform: translateX(789px);
}

.sequence-leave-to {
  transform: translateX(-789px);
}

.sequence-leave-active {
  position: absolute;
  top: 0;
  left: 0;
}
</style>