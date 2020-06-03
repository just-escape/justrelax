<template>
  <div class="position-absolute h-100 w-100 d-flex align-items-center justify-content-center" :class="{shrink: size === 'small'}">
    <div class="d-flex flex-row closed align-items-center">
      <NeonsWarning class="mx-3"/>
      <div>{{ $t('closed') }}</div>
      <NeonsWarning class="mx-3"/>
    </div>
  </div>
</template>

<script>
import NeonsWarning from '@/components/NeonsWarning.vue'

export default {
  name: "WarningClosed",
  components: {
    NeonsWarning,
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