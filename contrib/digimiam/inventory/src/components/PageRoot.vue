<template>
  <div class="h-100 position-relative">
    <BackgroundLines/>
    <div class="h-100 justify-content-center d-flex flex-column p-5">
      <div class="h-670px d-flex flex-row mb-5">
        <DecorationPanel class="w-55 mr-4"/>
        <Logs class="w-45 ml-4"/>
      </div>
      <Sokoban class="h-1250px"/>
      <DangerWindow/>
    </div>
  </div>
</template>

<script>
import BackgroundLines from '@/components/BackgroundLines.vue'
import DecorationPanel from '@/components/DecorationPanel.vue'
import Logs from '@/components/Logs.vue'
import Sokoban from '@/components/Sokoban.vue'
import DangerWindow from '@/components/DangerWindow.vue'

export default {
  name: 'PageRoot',
  components: {
    BackgroundLines,
    DecorationPanel,
    Logs,
    Sokoban,
    DangerWindow,
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
.h-670px {
  height: 670px;
}

.w-55 {
  width: 55%;
}

.w-45 {
  width: 45%;
}

.h-1250px {
  height: 1250px;
}

.w-360px {
  width: 360px;
}
</style>