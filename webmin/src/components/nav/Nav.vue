<template>
  <nav class="bgc-deepdark">
    <div class="position-sticky top-0 h-100vh">
      <div class="d-flex justify-content-between flex-column h-100vh">
        <div>
          <Brand></Brand>
          <Tabs></Tabs>
        </div>
        <div class="d-flex flex-row align-items-center justify-content-end p-2">
          <div class="mr-2">Mode maintenance</div>
          <div
            class="border mr-1 position-relative pointer"
            style="border-color: #ef8649 !important; height: 17px; width: 17px"
            @click="setMaintenanceMode(isInMaintenanceMode ? false : true)"
          >
            <i v-if="isInMaintenanceMode" class="position-absolute text-jaffa fa fa-xs fa-fw fa-check" style="bottom: 0; right: 0"></i>
          </div>
          <!--<LocaleSelector></LocaleSelector>-->
        </div>
      </div>
    </div>
  </nav>
</template>

<script>
import Brand from '@/components/nav/Brand.vue'
import Tabs from '@/components/nav/Tabs.vue'
// import LocaleSelector from '@/components/nav/LocaleSelector.vue'

import preferenceStore from '@/store/preferenceStore.js'

export default {
  name: 'Nav',
  components: {
    Brand,
    Tabs,
    // LocaleSelector,
  },
  computed: {
    isInMaintenanceMode() {
      return preferenceStore.state.isInMaintenanceMode
    },
  },
  methods: {
    setMaintenanceMode(value) {
      preferenceStore.commit('setMaintenanceMode', value)
      localStorage.setItem('isInMaintenanceMode', value)
    },
  },
  mounted() {
    preferenceStore.commit('setMaintenanceMode', JSON.parse(localStorage.getItem('isInMaintenanceMode')) ? true : false)
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
