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
      <BlackScreen/>
    </div>
  </div>
</template>

<script>
import BackgroundLines from '@/components/BackgroundLines.vue'
import DecorationPanel from '@/components/DecorationPanel.vue'
import Logs from '@/components/Logs.vue'
import Sokoban from '@/components/Sokoban.vue'
import DangerWindow from '@/components/DangerWindow.vue'
import BlackScreen from '@/components/BlackScreen.vue'

export default {
  name: 'PageRoot',
  components: {
    BackgroundLines,
    DecorationPanel,
    Logs,
    Sokoban,
    DangerWindow,
    BlackScreen,
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