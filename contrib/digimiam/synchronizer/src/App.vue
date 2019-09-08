<template>
  <div id="app">
    <LightSynchronizer/>
  </div>
</template>

<script>
import LightSynchronizer from './components/LightSynchronizer.vue'
// import roomStore from '@/store/roomStore.js'

export default {
  name: 'app',
  components: {
    LightSynchronizer
  },
  mounted() {
    // roomStore.dispatch('fetchRooms')
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
