<template>
  <div class="glowing-container">
    <div>
      <svg viewBox="90 0 423 252">
        <LightContainerDefs/>

        <LightContainerGenerator/>
        <LightContainerGenerator transform="translate(-20 0) rotate(180 335 178)"/>
        <LightContainerEdges/>
        <LightContainerVertice
          v-for="(v, verticeIndex) in vertices" :key="verticeIndex"
          :x="v.x"
          :y="v.y"
          :startingPoint="v.startingPoint"
          :r="v.color.r"
          :g="v.color.g"
          :b="v.color.b"
          :a="v.color.a"
          :glowing="v.glowing"
          :showGlobalError="showGlobalError"
          :pulse="v.pulse"
        />
      </svg>
    </div>
  </div>
</template>

<script>
import LightContainerDefs from '@/components/LightContainerDefs.vue'
import LightContainerGenerator from '@/components/LightContainerGenerator.vue'
import LightContainerEdges from '@/components/LightContainerEdges.vue'
import LightContainerVertice from '@/components/LightContainerVertice.vue'
import lightStore from '@/store/lightStore.js'

export default {
  name: 'LightContainer',
  components: {
    LightContainerDefs,
    LightContainerGenerator,
    LightContainerEdges,
    LightContainerVertice,
  },
  computed: {
    vertices() {
      return lightStore.state.vertices
    },
    showGlobalError() {
      return lightStore.state.showGlobalError
    },
  },
}
</script>

<style scoped>
svg {
  height: 470px;
}
</style>
