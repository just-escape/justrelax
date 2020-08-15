<template>
  <div
    class="triangle"
    :class="{
      'triangle-sm': size === 'sm',
      'triangle-md': size === 'md',
      'triangle-lg': size === 'lg',
    }"
    :style="{opacity: opacity}"
  >
  {{opacity}}
  </div>
</template>

<script>
export default {
  name: "LightMonitorUnitTriangle",
  props: {
    opacity: Number,
    size: {
      type: String,
      default: 'md',
    },
  }
}
</script>

<style scoped>
.triangle {
  background: white;
  clip-path: polygon(
    0% 0%,
    100% 0%,
    50% 100%
  );
  margin-bottom: 8px;
}

.triangle-sm {
  height: 10px;
  width: 20px;
}

.triangle-md {
  height: 15px;
  width: 30px;
}

.triangle-lg {
  height: 20px;
  width: 40px;
}
</style>