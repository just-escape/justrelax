<template>
  <nav class="bgc-deepdark">
    <div class="position-sticky top-0">
      <AppNavBrand></AppNavBrand>
      <AppNavTabs></AppNavTabs>
    </div>
  </nav>
</template>

<script>
import AppNavBrand from '@/components/AppNavBrand.vue'
import AppNavTabs from '@/components/AppNavTabs.vue'

export default {
  name: 'AppNav',
  components: {AppNavBrand, AppNavTabs},
}
</script>

<style scoped>
nav {
  width: 300px;
  z-index: 2;
}
</style>
