<template>
  <b-button :size="size" @click="$emit('click')">
    <slot></slot>
  </b-button>
</template>

<script>
export default {
  name: 'ButtonJaffa',
  props: ['size']
}
</script>

<style scoped>
button {
    background-color: transparent;
    color: #ef8649;
    border-color: #ef8649;
    transition: color 0.25s ease-in-out, background-color 0.25s ease-in-out;
}

button:disabled, button:hover:disabled {
  background-color: transparent;
  color: #949497;
  border-color: #949497;
}

button:hover:not(:disabled) {
    background-color: #ef8649;
    color: #3c3c3e;
    border-color: #ef8649;
}

button:not(:disabled):not(.disabled):active {
    background-color: #ef8649;
    color: #f8f9fa;
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
