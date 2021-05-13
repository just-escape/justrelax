<template>
  <div class="h-100 d-flex flex-column align-items-center">
    <Title/>
    <MenuFrame class="mb-4"/>
    <ButtonsBottom/>
  </div>
</template>

<script>
import Title from '@/components/Title.vue'
import MenuFrame from '@/components/MenuFrame.vue'
import ButtonsBottom from '@/components/ButtonsBottom.vue'

export default {
  name: 'PageRoot',
  components: {
    Title,
    MenuFrame,
    ButtonsBottom,
  },
  created() {
    let locale = this.$route.query.locale
    if (locale === undefined || locale === 'fr') {
      this.$i18n.locale = 'fr'
    } else {
      this.$i18n.locale = 'en'
    }
  },
}
</script>
