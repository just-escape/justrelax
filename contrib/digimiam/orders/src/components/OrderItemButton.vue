<template>
  <b-btn
    @mousedown="mousedown"
    variant="info rounded-circle"
    :disabled="disabled"
    :style="{transform: 'scale(' + scale + ')'}"
  >
    <div><i class="fas fa-plus"></i></div>
  </b-btn>
</template>

<script>
export default {
  name: "OrderItemButton",
  data() {
    return {
      scale: 1,
    }
  },
  methods: {
    mousedown: function() {
      this.$emit('mousedown')
      this.$anime.timeline({
        targets: this,
        easing: 'easeOutCubic',
        duration: 200,
      })
      .add({
        scale: 1.2,
      })
      .add({
        scale: 1,
      })
    },
  },
  props: ["disabled"]
}
</script>

<style scoped>
button {
  opacity: 0.75;
  filter: drop-shadow(0px 0px 4px rgba(23, 162, 184, 0.75));
  box-shadow: none !important;
}

button:disabled {
  opacity: 0.4;
}
</style>
