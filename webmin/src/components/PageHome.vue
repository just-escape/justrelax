<template>
  <AppContent>
    <AppContentTitle slot="header-left">
      Home
    </AppContentTitle>
    <div slot="main">home</div>
  </AppContent>
</template>

<script>
import AppContent from '@/components/AppContent.vue'
import AppContentTitle from '@/components/AppContentTitle.vue'

export default {
  name: 'PageHome',
  components: {
    AppContent,
    AppContentTitle
  }
}
</script>
