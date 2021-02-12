<template>
  <div
    @touchmove="cursorMove"
    @mousemove="cursorMove"
    @touchend="cursorRelease"
    @mouseup="cursorRelease"
    @mouseleave="mouseleave"
    @touchleave="mouseleave"
    class="d-flex justify-content-center position-relative h-100"
  >
    <BackgroundLines/>
    <div class="row py-5 px-5 w-100">
      <div class="col-9 pl-0 pr-4">
        <div class="d-flex flex-column h-100">
          <LightPuzzle class="h-50 mb-3"/>
          <MenuPuzzle class="h-50 mt-3"/>
        </div>
      </div>
      <div class="col-3 px-0">
        <Logs/>
      </div>
    </div>
    <OverlayVideo class="position-absolute z-index-20"/>
    <DangerWindow/>
  </div>
</template>

<script>
import BackgroundLines from '@/components/BackgroundLines.vue'
import LightPuzzle from '@/components/LightPuzzle.vue'
import MenuPuzzle from '@/components/MenuPuzzle.vue'
import OverlayVideo from '@/components/OverlayVideo.vue'
import DangerWindow from '@/components/DangerWindow.vue'
import Logs from '@/components/Logs.vue'
import menuStore from '@/store/menuStore.js'
import progressionStore from '@/store/progressionStore.js'

export default {
  name: 'PageRoot',
  components: {
    BackgroundLines,
    Logs,
    LightPuzzle,
    MenuPuzzle,
    OverlayVideo,
    DangerWindow,
  },
  data() {
    return {
      releaseTask: null,
    }
  },
  computed: {
    dragging() {
      return menuStore.state.dragging
    },
  },
  methods: {
    cursorMove: function(event) {
      menuStore.commit('appCursorMove', event)
    },
    cursorRelease: function() {
      clearTimeout(this.releaseTask)
      this.releaseTask = setTimeout(this._cursorRelease, 0.2)
    },
    _cursorRelease: function() {
      menuStore.commit('appCursorRelease')
    },
    mouseleave: function() {
      menuStore.commit('appMouseleave')
    },
  },
  watch: {
    dragging() {
      clearTimeout(this.releaseTask)
    },
  },
  created() {
    var lang = this.$route.query.lang
    if (lang === undefined || lang == 'fr') {
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
