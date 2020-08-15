<template>
  <div class="container-fluid px-0">
    <div class="row justify-content-center">
      <div class="w-small">
        <LightPuzzleMenu/>
      </div>
      <div class="w-large">
        <LightContainer/>
      </div>
    </div>
  </div>
</template>

<script>
import LightPuzzleMenu from '@/components/LightPuzzleMenu.vue'
import LightContainer from '@/components/LightContainer.vue'

export default {
  name: 'LightPuzzle',
  components: {
    LightPuzzleMenu,
    LightContainer,
  },
}
</script>