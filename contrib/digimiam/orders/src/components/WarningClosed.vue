<template>
  <div class="position-absolute h-100 w-100 d-flex align-items-center justify-content-center" :class="{shrink: size === 'small'}">
    <div class="d-flex flex-row closed align-items-center">
      <Neons class="mx-3" color="var(--warning)"/>
      <div>{{ $t('closed') }}</div>
      <Neons class="mx-3" color="var(--warning)"/>
    </div>
  </div>
</template>

<script>
import Neons from '@/components/Neons.vue'

export default {
  name: "WarningClosed",
  components: {
    Neons,
  },
  props: {
    size: {
      type: String,
      default: "normal",
    }
  }
}
</script>

<style scoped>
.closed {
  background-color: orangered;
  color: white;
  font-size: 40px;
  height: 65px;
  width: 400px;
  border-radius: 0.25rem;
  transform: rotate(-14deg);
}

.shrink {
  transform: scale(0.8);
}
</style>