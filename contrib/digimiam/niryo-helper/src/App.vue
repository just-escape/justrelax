<template>
  <div id="app" class="w-100 justify-content-center d-flex">
    <Token :configurationId="configurationId"/>
  </div>
</template>

<script>
import Token from './components/Token.vue'
import businessStore from '@/store/businessStore.js'

export default {
  name: 'App',
  components: {
    Token
  },
  computed: {
    configurationId() {
      return businessStore.state.displayedConfigurationId
    }
  },
  created() {
    this.$connect()
  }
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
