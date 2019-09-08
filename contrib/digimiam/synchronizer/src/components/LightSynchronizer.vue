<template>
  <div class="d-flex flex-row justify-content-center">
    <table>
      <thead>
      </thead>
      <tbody>
        <tr>
          <td v-for="light in lights" :key="light.id" class="py-3 px-2">
            <i v-if="light.validated" class="fas fa-check fa-fw"></i>
            <i v-else class="fas fa-times fa-fw"></i>
          </td>
        </tr>
        <tr>
          <td v-for="light in lights" :key="light.id" class="py-3 px-2">
            <i v-if="light.activated" class="fas fa-shoe-prints fa-fw"></i>
          </td>
        </tr>
        <tr>
          <td v-for="light in lights" :key="light.id" class="py-3 px-2">
            <i class="fas fa-circle fa-fw" :style="{color: light.color}"></i>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
import store from '@/store/store.js'

export default {
  name: 'LightSynchronizer',
  computed: {
    lights: function() {
      return store.state.lights
    }
  }
}
</script>

<style scoped>
table {
  font-size: 5rem;
  line-height: 1;
  background-color: darkgrey;
  color: black;
}
</style>
