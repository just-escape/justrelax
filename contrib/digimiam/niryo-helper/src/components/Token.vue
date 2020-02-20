<template>
  <div
    class="pl-1 pt-1"
  >
    <div
      v-for="(c, cIndex) in configuration"
      :key="cIndex"
      class="d-flex flex-row pb-1"
    >
      <div
        v-for="(r, rIndex) in c"
        :key="rIndex"
        class="d-flex flex-column mr-1"
        :class="{'bg-black': r, 'bg-grey': !r}"
        style="width: 50px; height: 50px"
      >
      </div>
    </div>
  </div>
</template>

<script>
import businessStore from '@/store/businessStore.js'

export default {
  name: "Token",
  computed: {
    configuration() {
      return businessStore.state.configurations[this.configurationId]
    }
  },
  props: {
    configurationId: String,
  },
}
</script>

<style scoped>
.bg-black {
  background: black;
}

.bg-grey {
  background: lightgrey;
}
</style>