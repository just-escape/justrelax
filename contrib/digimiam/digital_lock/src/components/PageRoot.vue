<template>
  <div
    @mousemove="mousemove"
    @touchmove="touchmove"
    @mouseup="release"
    @touchend="release"
    class="app-container d-flex flex-column justify-content-around align-items-center"
  >
    <Title class="mt-4"/>
    <DrawBox class="mt-3"/>
    <TextBottom class="align-self-end mr-4"/>
    <AlarmWindow/>
  </div>
</template>

<script>
import Title from '@/components/Title.vue'
import TextBottom from '@/components/TextBottom.vue'
import DrawBox from '@/components/DrawBox.vue'
import AlarmWindow from '@/components/AlarmWindow.vue'
import lockStore from '@/store/lockStore.js'

export default {
  name: 'PageRoot',
  components: {
    Title,
    DrawBox,
    TextBottom,
    AlarmWindow,
  },
  methods: {
    mousemove(event) {
      let x = event.clientX
      let y = event.clientY
      lockStore.commit('move', {x, y})
    },
    touchmove(event) {
      let x = event.targetTouches[0].clientX
      let y = event.targetTouches[0].clientY
      lockStore.commit('move', {x, y})
    },
    release() {
      if (!lockStore.state.lockActions) {
        if (lockStore.state.showErrorOnRealse) {
          lockStore.commit('setConnectorsColorTransition', 0.8)
          lockStore.commit('showError')
          setTimeout(lockStore.commit, 801, 'setConnectorsColorTransition', 0)
          setTimeout(lockStore.commit, 1200, 'resetPattern')
        } else {
          lockStore.commit('resetPattern')
        }
      }
    },
  },
  created() {
    var locale = this.$route.query.locale
    if (locale === undefined || locale == 'fr') {
      this.$i18n.locale = 'fr'
    } else {
      this.$i18n.locale = 'en'
    }
  },
}
</script>

<style scoped>
.app-container {
  width: 600px;
  height: 1024px;
}
</style>