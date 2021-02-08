<template>
  <ul class="list-unstyled mb-0 text-left">
    <li>
      <Tab :url="'/'" :icon="'fas fa-home'" :label="'Home'"/>
    </li>
    <li v-for="room in rooms" :key="room.id">
      <TabRoom :room="room"/>
    </li>
    <!--<li>
      <TabEditor/>
    </li>-->
  </ul>
</template>

<script>
import Tab from '@/components/nav/Tab.vue'
import TabRoom from '@/components/nav/TabRoom.vue'
// import TabEditor from '@/components/nav/TabEditor.vue'
import roomStore from '@/store/roomStore.js'

export default {
  name: 'Tabs',
  components: {
    Tab,
    TabRoom,
    // TabEditor,
  },
  computed: {
    rooms() {
      return roomStore.state.rooms ? roomStore.state.rooms : []
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
