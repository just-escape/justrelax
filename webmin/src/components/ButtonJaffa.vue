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

button:hover {
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
</style>
