<template>
  <div id="app">
    <LightSynchronizer/>
  </div>
</template>

<script>
import LightSynchronizer from './components/LightSynchronizer.vue'

export default {
  name: 'app',
  components: {
    LightSynchronizer
  },
  mounted() {
    this.$connect()
  }
}
</script>

<style>
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  margin-top: 60px;
}
</style>
