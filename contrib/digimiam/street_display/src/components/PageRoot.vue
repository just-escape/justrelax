<template>
  <div class="h-100 d-flex flex-column align-items-center">
    <Title/>
    <MenuFrame class="mb-4"/>
    <ButtonsBottom/>
    <!--<OverlayVideo/>-->
  </div>
</template>

<script>
//import OverlayVideo from '@/components/OverlayVideo.vue'
import Title from '@/components/Title.vue'
import MenuFrame from '@/components/MenuFrame.vue'
import ButtonsBottom from '@/components/ButtonsBottom.vue'

export default {
  name: 'PageRoot',
  components: {
    //OverlayVideo,
    Title,
    MenuFrame,
    ButtonsBottom,
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
