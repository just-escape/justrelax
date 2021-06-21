<template>
  <div
    class="glowing-container h-100 d-flex flex-column justify-content-between overflow-hidden position-relative"
  >
    <div class="overflow-hidden position-relative">
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
  computed: {
    units() {
      return lightStore.state.sequence
    },
  },
}
</script>

<style scoped>
.sequence-item {
  transition: all 1s linear;
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