<template>
  <div class="bg-dark h-100">
    <OverlayVideo/>
  </div>
</template>

<script>
import OverlayVideo from '@/components/OverlayVideo.vue'

export default {
  name: 'PageRoot',
  components: {
    OverlayVideo,
  },
  created() {
    let lang = this.$route.query.lang
    if (lang === undefined || lang === 'fr') {
      this.$i18n.locale = 'fr'
    } else {
      this.$i18n.locale = 'en'
    }
  },
}
</script>
