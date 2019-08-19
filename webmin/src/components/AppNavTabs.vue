<template>
  <ul class="list-unstyled mb-0 text-left">
    <li>
      <AppNavTab :url="'/'" :icon="'fas fa-home'" :label="'Home'"/>
    </li>
    <li>
      <AppNavTabRoom/>
    </li>
    <li>
      <AppNavTab :url="'/scores'" :icon="'far fa-id-card'" :label="'Scores'"/>
    </li>
    <li>
      <AppNavTab :url="'/stats'" :icon="'far fa-chart-bar'" :label="'Statistics'"/>
    </li>
    <li>
      <AppNavTab :url="'/editor'" :icon="'far fa-file-code'" :label="'Editor'"/>
    </li>
  </ul>
</template>

<script>
import AppNavTab from '@/components/AppNavTab.vue'
import AppNavTabRoom from '@/components/AppNavTabRoom.vue'

export default {
  name: 'AppNavTabs',
  components: {
    AppNavTab,
    AppNavTabRoom
  }
}
</script>

<style scoped>
ul > li:first-child {
  border-top: 1px solid #3c3c3e;
}

ul > li {
  border-bottom: 1px solid #3c3c3e;
}
</style>
