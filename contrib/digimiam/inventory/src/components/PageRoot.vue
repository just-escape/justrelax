<template>
  <div
    @mousemove="mousemove"
    @mouseup="mouseup"
    @mouseleave="mouseleave"
    class="h-100 justify-content-center d-flex position-relative"
  >
    <BackgroundLines/>
    <div class="padding-top-10px">
      <Container/>
    </div>
  </div>
</template>

<script>
import BackgroundLines from '@/components/BackgroundLines.vue'
import Container from '@/components/Container.vue'
import blockStore from '@/store/blockStore.js'

export default {
  name: 'PageRoot',
  components: {
    BackgroundLines,
    Container,
  },
  methods: {
    mousemove: function(event) {
      blockStore.commit('appMousemove', event)
    },
    mouseup: function() {
      blockStore.commit('appMouseup')
    },
    mouseleave: function() {
      blockStore.commit('appMouseleave')
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
