<template>
  <div class="position-relative h-100">
    <Scene class="position-absolute"/>
    <ItemSelector class="position-absolute"/>
    <OrderSummary class="position-absolute order-summary"/>
    <OverlayVideo class="position-absolute"/>
  </div>
</template>

<script>
import Scene from '@/components/Scene.vue'
import ItemSelector from '@/components/ItemSelector.vue'
import OrderSummary from '@/components/OrderSummary.vue'
import OverlayVideo from '@/components/OverlayVideo.vue'

export default {
  name: 'PageRoot',
  components: {
    Scene,
    ItemSelector,
    OrderSummary,
    OverlayVideo,
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

<style scoped>
.order-summary {
  bottom: 0px;
  right: 0px;
  width: 500px;
  height: 294px;
}
</style>
