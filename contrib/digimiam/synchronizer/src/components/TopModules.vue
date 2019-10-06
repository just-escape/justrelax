<template>
  <div class="container-fluid">
    <div class="h-400px row">
      <div class="col-9">
        <LightContainer/>
      </div>
      <div class="col-3">
        <Logs/>
      </div>
    </div>
  </div>
</template>

<script>
import LightContainer from '@/components/LightContainer.vue'
import Logs from '@/components/Logs.vue'

export default {
  name: 'TopModules',
  components: {
    LightContainer,
    Logs,
  },
}
</script>

<style scoped>
.h-400px {
  height: 400px
}
</style>
