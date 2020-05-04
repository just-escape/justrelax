<template>
  <div class="container-fluid px-0">
    <div class="row justify-content-center">
      <div class="col-3">
        <LightPuzzleMenu/>
      </div>
      <div class="col-8">
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