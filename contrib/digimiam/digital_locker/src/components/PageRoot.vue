<template>
  <div class="app-container d-flex flex-column justify-content-center align-items-center">
    <BackgroundLines/>
    <Title class="mb-5"/>
    <DrawBox class="mb-4 mt-3"/>
    <TextBottom class="align-self-end mr-4"/>
  </div>
</template>

<script>
import BackgroundLines from '@/components/BackgroundLines.vue'
import Title from '@/components/Title.vue'
import TextBottom from '@/components/TextBottom.vue'
import DrawBox from '@/components/DrawBox.vue'

export default {
  name: 'PageRoot',
  components: {
    BackgroundLines,
    Title,
    DrawBox,
    TextBottom,
  },
  created() {
    var lang = this.$route.query.lang
    if (lang === undefined || lang == 'fr') {
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