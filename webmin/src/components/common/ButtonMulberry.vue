<template>
  <b-button @click="$emit('click')" :class="this.getClasses">
    <slot></slot>
  </b-button>
</template>

<script>
export default {
  name: 'ButtonMulberry',
  computed: {
    getClasses() {
      if (this.active) {
        return 'filled'
      } else {
        return ''
      }
    }
  },
  props: ['active']
}
</script>

<style scoped>
button {
    background-color: transparent;
    color: #cb4299;
    border-color: #cb4299;
    transition: color 0.25s ease-in-out, background-color 0.25s ease-in-out;
}

button:hover, .filled {
    background-color: #cb4299;
    color: #3c3c3e;
    border-color: #cb4299;
}

button:not(:disabled):not(.disabled):active {
    background-color: #cb4299;
    color: #f8f9fa;
}

button:focus, button:not(:disabled):not(.disabled):active:focus {
    box-shadow: none;
}
</style>
