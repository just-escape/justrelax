<template>
  <div class="d-flex flex-row justify-content-between glowing-container">
    <LightContainerTmpControls/>
    <div>
      <svg viewBox="0 0 800 400">
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
import LightContainerTmpControls from '@/components/LightContainerTmpControls.vue'
import LightContainerEdges from '@/components/LightContainerEdges.vue'
import LightContainerVertices from '@/components/LightContainerVertices.vue'
import LightStore2 from '@/store/LightStore2.js'

export default {
  name: 'LightContainer',
  components: {
    LightContainerDefs,
    LightContainerGenerator,
    LightContainerTmpControls,
    LightContainerEdges,
    LightContainerVertices,
  },
  mounted() {
    LightStore2.dispatch('init')
  }
}
</script>

<style scoped>
svg {
  height: 400px;
  width: 800px;
}
</style>
