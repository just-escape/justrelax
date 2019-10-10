<template>
  <div class="container px-0">
    <div class="row">
      <div class="col-3">
        <LightPuzzleMenu/>
      </div>
      <div class="col-9">
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