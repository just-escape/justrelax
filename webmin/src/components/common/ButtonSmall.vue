<template>
  <b-button size="sm" @click="$emit('click')">
    <slot></slot>
  </b-button>
</template>

<script>
export default {
  name: "ButtonSmall"
}
</script>

<style scoped>
button {
  font-size: 0.8rem;
  background-color: transparent;
  color: #f8f9fa;
  border-color: #f8f9fa;
  transition: color 0.25s ease-in-out, background-color 0.25s ease-in-out;
}

button:disabled, button:hover:disabled {
  background-color: transparent;
  color: #949497;
  border-color: #949497;
}

button:hover:not(:disabled) {
  background-color: #f8f9fa;
  color: #3c3c3e;
  border-color: #f8f9fa;
}

button:not(:disabled):not(.disabled):active {
  background-color: #f8f9fa;
  color: #3c3c3e;
}

button:focus, button:not(:disabled):not(.disabled):active:focus {
  box-shadow: none;
}

.btn-group > .btn:not(:last-child):disabled,
.btn-group > .btn:not(:last-child):hover:disabled {
  border-right-color: transparent;
}

.btn-group > .btn:not(:first-child):disabled,
.btn-group > .btn:not(:first-child):hover:disabled {
  border-left-color: transparent;
}
</style>