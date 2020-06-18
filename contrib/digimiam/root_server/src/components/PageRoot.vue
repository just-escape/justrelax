<template>
  <div class="position-relative h-100">
    <BackgroundLines/>

    <div class="d-flex flex-row h-100 p-5">
      <div class="d-flex flex-column w-25 pr-4">
        <div class="d-flex flex-row h-50 mb-4">
          <ServicesWindow/>
        </div>
        <div class="d-flex flex-row h-50 mt-4">
          <ConfigurationWindow/>
        </div>
      </div>

      <div class="d-flex flex-column w-50 px-4">
        <div class="d-flex flex-row h-75 mb-4">
          <MarmitronWindow/>
        </div>
        <div class="d-flex flex-row h-25">
          <Keyboard/>
        </div>
      </div>

      <div class="d-flex flex-column w-25 pl-4">
        <div class="d-flex flex-row h-50 mb-4">
          <MenuWindow/>
        </div>
        <div class="d-flex flex-row h-50 mt-4">
          <AdsWindow/>
        </div>
      </div>
    </div>

    <PasswordWindow/>
    <PasswordRecoveryWindow/>
    <DangerWindow/>

    <ExpandableVideos/>
  </div>
</template>

<script>
import BackgroundLines from '@/components/BackgroundLines.vue'
import PasswordWindow from '@/components/PasswordWindow.vue'
import PasswordRecoveryWindow from '@/components/PasswordRecoveryWindow.vue'
import DangerWindow from '@/components/DangerWindow.vue'
import ExpandableVideos from '@/components/ExpandableVideos.vue'
import MarmitronWindow from '@/components/MarmitronWindow.vue'
import ServicesWindow from '@/components/ServicesWindow.vue'
import ConfigurationWindow from '@/components/ConfigurationWindow.vue'
import AdsWindow from '@/components/AdsWindow.vue'
import MenuWindow from '@/components/MenuWindow.vue'
import Keyboard from '@/components/Keyboard.vue'

export default {
  name: 'PageRoot',
  components: {
    BackgroundLines,
    ExpandableVideos,
    PasswordWindow,
    PasswordRecoveryWindow,
    DangerWindow,
    MarmitronWindow,
    ServicesWindow,
    ConfigurationWindow,
    AdsWindow,
    MenuWindow,
    Keyboard,
  },
  created() {
    var lang = this.$route.query.lang
    if (lang === undefined || lang == 'fr') {
      this.$i18n.locale = 'fr'
    } else {
      this.$i18n.locale = 'en'
    }
  }
}
</script>
