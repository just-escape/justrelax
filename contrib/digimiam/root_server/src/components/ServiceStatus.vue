<template>
  <div class="d-flex flex-column align-items-center">
    <div class="position-relative mb-1" :style="{opacity: opacity}">
      <slot></slot>
      <i v-if="!error" class="position-absolute fas fa-check status-mark"/>
      <i v-else class="position-absolute fas fa-times status-mark-error"/>
    </div>
    <div>
      {{ label }}
    </div>
  </div>
</template>

<script>
export default {
  name: "ServiceStatus",
  data() {
    return {
      opacity: 0.75,
    }
  },
  watch: {
    error(newValue) {
      if (newValue) {
        this.$anime({
          targets: this,
          opacity: 0,
          duration: 1,
          delay: 100,
          endDelay: 120,
          loop: true,
          direction: 'alternate',
          easing: 'easeInQuad',
        })
      }
    },
  },
  props: {
    label: String,
    error: {
      type: Boolean,
      default: false,
    },
  },
}
</script>

<style scoped>
.status-mark {
  bottom: 0px;
  right: -10px;
  font-size: 20px;
  color: green;
}

.status-mark-error {
  bottom: 0px;
  right: -10px;
  font-size: 20px;
  color: rgb(230, 0, 40);
}
</style>