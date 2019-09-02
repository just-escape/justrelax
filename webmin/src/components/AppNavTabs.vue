<template>
  <ul class="list-unstyled mb-0 text-left">
    <li>
      <AppNavTab :url="'/'" :icon="'fas fa-home'" :label="'Home'"/>
    </li>
    <li v-for="room in rooms" :key="room.id">
      <AppNavTabRoom :room="room"/>
    </li>
    <li>
      <AppNavTab :url="'/medias'" :icon="'fas fa-music'" :label="'Medias'"/>
    </li>
  </ul>
</template>

<script>
import AppNavTab from '@/components/AppNavTab.vue'
import AppNavTabRoom from '@/components/AppNavTabRoom.vue'
import roomStore from '@/store/roomStore.js'

export default {
  name: 'AppNavTabs',
  components: {
    AppNavTab,
    AppNavTabRoom,
  },
  computed: {
    rooms: function() {
      return roomStore.state.rooms
    }
  },
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
