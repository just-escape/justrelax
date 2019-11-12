<template>
  <AppContent>
    <AppContentTitle slot="header-left">
      Settings
    </AppContentTitle>
    <div slot="main">
      <General class="mb-5"/>
      <Cameras/>
    </div>
  </AppContent>
</template>

<script>
import AppContent from '@/components/common/AppContent.vue'
import AppContentTitle from '@/components/common/AppContentTitle.vue'
import General from '@/components/settings/General.vue'
import Cameras from '@/components/settings/Cameras.vue'

export default {
  name: 'PageSettings',
  components: {
    AppContent,
    AppContentTitle,
    General,
    Cameras,
  },
  props: ['roomId']
}
</script>
