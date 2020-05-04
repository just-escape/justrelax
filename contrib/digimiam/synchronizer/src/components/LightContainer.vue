<template>
  <div class="glowing-container">
    <div>
      <svg viewBox="0 0 600 400">
        <LightContainerDefs/>

        <LightContainerGenerator/>
        <LightContainerEdges/>
        <LightContainerVertices/>
      </svg>
    </div>
  </div>
</template>

<script>
import LightContainerDefs from '@/components/LightContainerDefs.vue'
import LightContainerGenerator from '@/components/LightContainerGenerator.vue'
import LightContainerEdges from '@/components/LightContainerEdges.vue'
import LightContainerVertices from '@/components/LightContainerVertices.vue'
import lightStore from '@/store/lightStore.js'

export default {
  name: 'LightContainer',
  components: {
    LightContainerDefs,
    LightContainerGenerator,
    LightContainerEdges,
    LightContainerVertices,
  },
  mounted() {
    lightStore.dispatch('init')
  }
}
</script>

<style scoped>
svg {
  height: 470px;
}
</style>
