<template>
  <AppContent>
    <AppContentTitle slot="header-left">
      Statistics
    </AppContentTitle>
    <div slot="main">stats</div>
  </AppContent>
</template>

<script>
import AppContent from '@/components/common/AppContent.vue'
import AppContentTitle from '@/components/common/AppContentTitle.vue'

export default {
  name: 'PageStats',
  components: {
    AppContent,
    AppContentTitle
  },
  props: ['roomId']
}
</script>
