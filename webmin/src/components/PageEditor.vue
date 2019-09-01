<template>
  <AppContent>
    <AppContentTitle slot="header-left">
      Editor
    </AppContentTitle>
    <div slot="main">editor</div>
  </AppContent>
</template>

<script>
import AppContent from '@/components/AppContent.vue'
import AppContentTitle from '@/components/AppContentTitle.vue'

export default {
  name: 'PageEditor',
  components: {
    AppContent,
    AppContentTitle
  },
  props: ['roomId']
}
</script>
