<template>
  <div>
    <input type="checkbox" @click="toggleSensor('pink')"><span style="color: rgb(232, 62, 140)">Pink</span>
    <br>
    <input type="checkbox" @click="toggleSensor('orange')"><span style="color: rgb(253, 126, 20)">Orange</span>
    <br>
    <input type="checkbox" @click="toggleSensor('yellow')"><span style="color: rgb(255, 193, 7)">Yellow</span>
    <br>
    <input type="checkbox" @click="toggleSensor('green')"><span style="color: rgb(40, 167, 69)">Green</span>
    <br>
    <input type="checkbox" @click="toggleSensor('blue')"><span style="color: rgb(0, 123, 255)">Blue</span>
    <br>
    <input type="checkbox" @click="toggleSensor('purple')"><span style="color: rgb(102, 16, 242)">Purple</span>
  </div>
</template>

<script>
import LightStore2 from '@/store/LightStore2.js'

export default {
  name: 'LightContainerTmpControls',
  methods: {
    toggleSensor: function(sensorId) {
      LightStore2.dispatch('toggleSensor', sensorId)
    }
  }
}
</script>