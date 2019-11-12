<template>
  <nav class="bgc-deepdark">
    <div class="position-sticky top-0">
      <Brand></Brand>
      <Tabs></Tabs>
    </div>
  </nav>
</template>

<script>
import Brand from '@/components/nav/Brand.vue'
import Tabs from '@/components/nav/Tabs.vue'

export default {
  name: 'Nav',
  components: {Brand, Tabs},
}
</script>

<style scoped>
nav {
  width: 300px;
  z-index: 2;
}
</style>
