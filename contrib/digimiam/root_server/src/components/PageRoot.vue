<template>
  <div class="position-relative h-100">
    <BackgroundLines/>

    <div v-if="controls" class="position-absolute" style="font-size: 40px; top: 0; left: 0">
      <span @click="showUI" class="mr-5">interface</span>
      <span @click="showPassword" class="mr-5">password</span>
      <span @click="beer" class="mr-5">bière</span>
      <span @click="reponse" class="mr-5">réponse</span>
      <span @click="liberation">liberation</span>
    </div>

    <div class="d-flex flex-row h-100 p-5">
      <div class="d-flex flex-column w-25 pr-4" style="transition: opacity 5s ease-in-out" :style="{opacity: UIOpacity}" :class="{'d-none': !UIOpacity}">
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

      <div class="d-flex flex-column w-25 pl-4" style="transition: opacity 5s ease-in-out" :style="{opacity: UIOpacity}" :class="{'d-none': !UIOpacity}">
        <MenuWindow/>
      </div>
    </div>

    <PasswordWindow/>
    <PasswordRecoveryWindow/>
    <AlarmWindow/>
    <DangerWindow/>
    <OverlayVideo/>
  </div>
</template>

<script>
import BackgroundLines from '@/components/BackgroundLines.vue'
import PasswordWindow from '@/components/PasswordWindow.vue'
import PasswordRecoveryWindow from '@/components/PasswordRecoveryWindow.vue'
import AlarmWindow from '@/components/AlarmWindow.vue'
import DangerWindow from '@/components/DangerWindow.vue'
import MarmitronWindow from '@/components/MarmitronWindow.vue'
import ServicesWindow from '@/components/ServicesWindow.vue'
import ConfigurationWindow from '@/components/ConfigurationWindow.vue'
import MenuWindow from '@/components/MenuWindow.vue'
import Keyboard from '@/components/Keyboard.vue'
import OverlayVideo from '@/components/OverlayVideo.vue'
import businessStore from '@/store/businessStore.js'

export default {
  name: 'PageRoot',
  components: {
    BackgroundLines,
    PasswordWindow,
    PasswordRecoveryWindow,
    AlarmWindow,
    DangerWindow,
    MarmitronWindow,
    ServicesWindow,
    ConfigurationWindow,
    MenuWindow,
    Keyboard,
    OverlayVideo,
  },
  computed: {
    controls() {
      let controls = this.$route.query.controls
      if (controls && controls == 1) {
        return true
      } else {
        return false
      }
    },
    UIOpacity() {
      return businessStore.state.showUI ? 1 : 0
    },
  },
  methods: {
    showUI() {
      businessStore.commit('showUI')
    },
    showPassword() {
      businessStore.commit('displayPasswordWindow')
    },
    beer() {
      businessStore.commit('playAnimation', 'beer')
    },
    reponse() {
      businessStore.commit('playAnimation', 'reponse')
    },
    liberation() {
      businessStore.commit('playAnimation', 'liberation')
    },
  },
  created() {
    var locale = this.$route.query.locale
    if (locale === undefined || locale == 'fr') {
      this.$i18n.locale = 'fr'
    } else {
      this.$i18n.locale = 'en'
    }
  }
}
</script>
