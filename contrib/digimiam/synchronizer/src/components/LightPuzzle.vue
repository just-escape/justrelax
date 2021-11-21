<template>
  <div class="container-fluid px-0">
    <div class="row justify-content-center">
      <div class="w-small" @click="click">
        <LightPuzzleMenu/>
      </div>
      <div class="w-large" @click="click" style="height: 470px">
        <LightContainer/>
      </div>
    </div>
  </div>
</template>

<script>
import LightPuzzleMenu from '@/components/LightPuzzleMenu.vue'
import LightContainer from '@/components/LightContainer.vue'
import lightLogStore from '@/store/lightLogStore.js'

export default {
  name: 'LightPuzzle',
  components: {
    LightPuzzleMenu,
    LightContainer,
  },
  data() {
    return {
      clickCounter: 0
    }
  },
  methods: {
    click() {
      this.clickCounter++
      if (this.clickCounter === 10) {
        lightLogStore.commit("processLog", {logMessage: "interface_is_not_tactile", level: "warning", useLocale: true, withSound: true})
      }
    }
  }
}
</script>