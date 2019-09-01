<template>
  <AppContent>
    <AppContentTitle slot="header-left">
      Score
    </AppContentTitle>
    <div slot="main">score</div>
  </AppContent>
</template>

<script>
import AppContent from '@/components/AppContent.vue'
import AppContentTitle from '@/components/AppContentTitle.vue'

export default {
  name: 'PageScore',
  components: {
    AppContent,
    AppContentTitle
  },
  props: ['roomId']
}
</script>
