<template>
  <b-button variant="dark" :size="size">
    <slot></slot>
  </b-button>
</template>

<script>
export default {
  name: 'UnclickableDarkButton',
  props: {
    'size': {
      default: "md"
    },
  }
}
</script>

<style scoped>
button:hover:not(:disabled) {
  background-color: var(--info);
  cursor: default;
  color: var(--info);
  border-color: var(--info);
}

button:focus, button:not(:disabled):not(.disabled):active:focus {
  background-color: var(--info);
  box-shadow: none;
  color: var(--info);
  border-color: var(--info);
}
</style>
