<template>
  <AppContent>
    <AppContentTitle slot="header-left">
      Home
    </AppContentTitle>
    <div slot="main">
      <!--<Rooms/>-->
    </div>
  </AppContent>
</template>

<script>
import AppContent from '@/components/common/AppContent.vue'
import AppContentTitle from '@/components/common/AppContentTitle.vue'
// import Rooms from '@/components/home/Rooms.vue'

export default {
  name: 'PageHome',
  components: {
    AppContent,
    AppContentTitle,
    // Rooms,
  }
}
</script>
