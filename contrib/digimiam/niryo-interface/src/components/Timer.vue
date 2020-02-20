<template>
  <div class="mx-3 d-flex flex-column h-100" style="width: 80px;">
    <TimeUnit
      v-for="(tu, index) in timeUnits"
      :key="index"
      class="mb-1"
      :active="tu"
    />
  </div>
</template>

<script>
import TimeUnit from '@/components/TimeUnit.vue'

export default {
  name: "Timer",
  components: {
    TimeUnit,
  },
  props: {
    timeUnits: Array,
  }
}
</script>