<template>
  <div class="position-relative h-100">
    <div class="container-fluid d-flex flex-column h-100">
      <div class="row h-100">
        <div class="col-4">
          <Selector class="row h-100"/>
        </div>
        <div class="col-5">
          <Marmitron class="mb-5"/>
        </div>
        <div class="col-3">
          <RightPanel/>
        </div>
      </div>
    </div>
    <!--<div class="container-fluid d-flex flex-column h-100">
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
    <WarningMessage class="top-0 position-absolute h-100 w-100"/>-->
  </div>
</template>

<script>
import Marmitron from '@/components/Marmitron.vue'
import RightPanel from '@/components/RightPanel.vue'
import Selector from '@/components/Selector.vue'

export default {
  name: 'PageRoot',
  components: {
    Marmitron,
    RightPanel,
    Selector,
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
.top-0 {
  top: 0;
}
</style>
