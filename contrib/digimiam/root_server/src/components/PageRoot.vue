<template>
  <div class="d-flex justify-content-center position-relative h-100">
    <Background/>
    <PasswordWindow/>
  </div>
</template>

<script>
import Background from '@/components/Background.vue'
import PasswordWindow from '@/components/PasswordWindow.vue'

export default {
  name: 'PageRoot',
  components: {
    Background,
    PasswordWindow,
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
