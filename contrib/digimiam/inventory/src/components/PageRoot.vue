<template>
  <div class="h-100 position-relative">
    <BackgroundLines/>
    <div class="h-100 justify-content-center d-flex flex-column p-5">
      <div class="h-640px d-flex flex-row mb-5">
        <DecorationPanel class="w-55 mr-4"></DecorationPanel>
        <Logs class="ml-4 flex-grow-1"/>
      </div>
      <Sokoban class="h-1280px"/>
      <!--<div class="padding-top-10px">
        <Container/>
      </div>-->
    </div>
  </div>
</template>

<script>
import BackgroundLines from '@/components/BackgroundLines.vue'
import DecorationPanel from '@/components/DecorationPanel.vue'
import Logs from '@/components/Logs.vue'
import Sokoban from '@/components/Sokoban.vue'
// import Container from '@/components/Container.vue'
// import blockStore from '@/store/blockStore.js'

export default {
  name: 'PageRoot',
  components: {
    BackgroundLines,
    DecorationPanel,
    Logs,
    Sokoban,
    // Container,
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
.h-640px {
  height: 640px;
}

.w-55 {
  width: 55%;
}

.h-1280px {
  height: 1280px;
}

.w-360px {
  width: 360px;
}
</style>