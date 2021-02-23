<template>
  <div class="position-relative overflow-hidden h-100">
    <Scene class="position-absolute"/>
    <ItemSelector class="position-absolute"/>
    <OrderSummary class="position-absolute order-summary"/>
    <VentilatorsDocumentation class="position-absolute"/>
    <OverlayVideo class="position-absolute"/>
    <DangerWindow/>
  </div>
</template>

<script>
import Scene from '@/components/Scene.vue'
import ItemSelector from '@/components/ItemSelector.vue'
import OrderSummary from '@/components/OrderSummary.vue'
import VentilatorsDocumentation from '@/components/VentilatorsDocumentation.vue'
import OverlayVideo from '@/components/OverlayVideo.vue'
import DangerWindow from '@/components/DangerWindow.vue'
import progressionStore from '@/store/progressionStore.js'

export default {
  name: 'PageRoot',
  components: {
    Scene,
    ItemSelector,
    OrderSummary,
    VentilatorsDocumentation,
    OverlayVideo,
    DangerWindow,
  },
  created() {
    var locale = this.$route.query.locale
    if (locale === undefined || locale == 'fr') {
      this.$i18n.locale = 'fr'
    } else {
      this.$i18n.locale = 'en'
    }
  },
  mounted() {
    let video = this.$route.query.video
    if (video !== "0") {
      progressionStore.commit('playOverlayVideo', 'glitching')
    }
  },
}
</script>

<style scoped>
.order-summary {
  bottom: 0px;
  right: 0px;
  width: 500px;
  height: 294px;
}
</style>
