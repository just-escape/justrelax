<template>
  <div class="d-flex flex-column align-items-center">
    <div class="position-relative mb-1 opacity-75">
      <slot></slot>
      <i class="position-absolute fas fa-check status-mark"/>
    </div>
    <div>
      {{ label }}
    </div>
  </div>
</template>

<script>
export default {
  name: "ServiceStatus",
  props: {
    label: String,
  },
}
</script>

<style scoped>
.opacity-75 {
  opacity: 0.75;
}

.status-mark {
  bottom: 0px;
  right: -10px;
  font-size: 20px;
  color: green;
}
</style>