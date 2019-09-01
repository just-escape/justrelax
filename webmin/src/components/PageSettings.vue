<template>
  <AppContent>
    <AppContentTitle slot="header-left">
      Settings
    </AppContentTitle>
    <div slot="main">
      <PageSettingsGeneral class="mb-5"/>
      <PageSettingsCameras/>
    </div>
  </AppContent>
</template>

<script>
import AppContent from '@/components/AppContent.vue'
import AppContentTitle from '@/components/AppContentTitle.vue'
import PageSettingsGeneral from '@/components/PageSettingsGeneral.vue'
import PageSettingsCameras from '@/components/PageSettingsCameras.vue'

export default {
  name: 'PageSettings',
  components: {
    AppContent,
    AppContentTitle,
    PageSettingsGeneral,
    PageSettingsCameras,
  },
  props: ['roomId']
}
</script>
