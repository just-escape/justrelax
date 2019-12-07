<template>
  <div class="container-fluid d-flex flex-column h-100">
    <Header/>
    <div class="row flex-grow-1">
      <div class="col-9 bg-light pt-3 pb-4">
        <LeftPanel/>
      </div>
      <div class="col-3 bg-light pt-3 pb-4">
        <RightPanel/>
      </div>
    </div>
  </div>
</template>

<script>
import Header from '@/components/Header.vue'
import LeftPanel from '@/components/LeftPanel.vue'
import RightPanel from '@/components/RightPanel.vue'

export default {
  name: 'PageRoot',
  components: {
    Header,
    LeftPanel,
    RightPanel,
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
