<template>
  <b-alert show>
    <button class="ml-3 close" @click="$emit('close')">×</button>
    <slot></slot>
  </b-alert>
</template>

<script>
export default {
  name: 'AlertMulberry',
}
</script>

<style scoped>
.alert {
  color: #cb4299;
  background-color: #3c3c3e;
  border-color: #cb4299;
}

.close {
  color: #cb4299;
  text-shadow: 1px 1px 0 #555;
  opacity: 0.8;
  outline-color: transparent;
}
</style>
