<template>
  <b-button variant="outline-primary">
    <slot></slot>
  </b-button>
</template>

<script>
export default {
  name: 'UnclickableOutlinePrimaryButton'
}
</script>

<style scoped>
button:hover:not(:disabled) {
  background-color: transparent;
  cursor: default;
  color: var(--primary);
}

button:focus, button:not(:disabled):not(.disabled):active:focus {
  background-color: transparent;
  box-shadow: none;
  color: var(--primary);
}
</style>
