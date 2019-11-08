<template>
  <div
    v-touch:moving="moving"
    v-touch:end="tapEnd"
    @mouseleave="mouseleave"
    class="d-flex justify-content-center position-relative h-100"
  >
    <BackgroundLines/>
    <div class="padding-top-10px global-container row py-3">
      <div class="col-9">
        <div class="d-flex flex-column">
          <LightPuzzle class="h-402px mb-4"/>
          <MenuPuzzle class="h-492px"/>
        </div>
      </div>
      <div class="col-3">
        <Logs/>
      </div>
    </div>
  </div>
</template>

<script>
import BackgroundLines from '@/components/BackgroundLines.vue'
import LightPuzzle from '@/components/LightPuzzle.vue'
import MenuPuzzle from '@/components/MenuPuzzle.vue'
import Logs from '@/components/Logs.vue'
import menuStore from '@/store/menuStore.js'

export default {
  name: 'PageRoot',
  components: {
    BackgroundLines,
    Logs,
    LightPuzzle,
    MenuPuzzle,
  },
  methods: {
    moving: function(event) {
      menuStore.commit('appMoving', event)
    },
    tapEnd: function() {
      menuStore.commit('appTapEnd')
    },
    mouseleave: function() {
      menuStore.commit('appMouseleave')
    },
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
