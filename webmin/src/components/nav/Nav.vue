<template>
  <nav class="bgc-deepdark">
    <div class="position-sticky top-0 h-100vh">
      <div class="d-flex justify-content-between flex-column h-100vh">
        <div>
          <Brand></Brand>
          <Tabs></Tabs>
        </div>
        <div>
          <LocaleSelector></LocaleSelector>
        </div>
      </div>
    </div>
  </nav>
</template>

<script>
import Brand from '@/components/nav/Brand.vue'
import Tabs from '@/components/nav/Tabs.vue'
import LocaleSelector from '@/components/nav/LocaleSelector.vue'

export default {
  name: 'Nav',
  components: {
    Brand,
    Tabs,
    LocaleSelector,
  },
}
</script>

<style scoped>
nav {
  width: 300px;
  z-index: 2;
}

.h-100vh {
  height: 100vh;
}
</style>
