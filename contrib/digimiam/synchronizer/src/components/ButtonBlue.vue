<template>
  <b-button @click="$emit('click')" class="position-relative">
    <div class="corner-top-left"></div>
    <div class="corner-top-right"></div>
    <div class="corner-bottom-left"></div>
    <div class="corner-bottom-right"></div>

    <slot></slot>
  </b-button>
</template>

<script>
export default {
  name: 'ButtonBlue',
}
</script>

<style scoped>
button {
    background-color: rgba(00, 45, 80, 0.6);
    color: rgba(0, 209, 182, 0.7);
    border-top: none;
    border-bottom: none;
    border-right: 3px solid rgba(0, 209, 182, 0.4);
    border-left: 3px solid rgba(0, 209, 182, 0.4);
    border-radius: 0px;
    transition: color 0.25s ease-in-out, background-color 0.25s ease-in-out;
}

button:hover:not(:disabled) {
    background-color: rgba(00, 209, 182, 0.1);
    border-right-color: rgba(0, 209, 182, 0.4);
    border-left-color: rgba(0, 209, 182, 0.4);
    color: rgba(0, 209, 182, 0.7);
}

button:not(:disabled):not(.disabled):active {
    background-color: rgba(00, 209, 182, 0.1);
    border-right-color: rgba(0, 209, 182, 0.4);
    border-left-color: rgba(0, 209, 182, 0.4);
    color: rgba(0, 209, 182, 0.7);
}

button:focus, button:not(:disabled):not(.disabled):active:focus {
  box-shadow: none;
}

.corner-top-left {
  position: absolute;
  width: 3px;
  border-top: 3px solid rgba(0, 209, 182, 0.6);
  top: 0;
  left: 0px;
}

.corner-top-left::before {
  position: absolute;
  content: '';
  width: 3px;
  border-top: 3px solid rgba(0, 209, 182, 0.35);
  top: -3px;
  left: -3px;
}

.corner-top-right {
  position: absolute;
  width: 3px;
  border-top: 3px solid rgba(0, 209, 182, 0.6);
  top: 0px;
  right: 0px;
}

.corner-top-right::before {
  position: absolute;
  content: '';
  width: 3px;
  border-top: 3px solid rgba(0, 209, 182, 0.35);
  top: -3px;
  right: -3px;
}

.corner-bottom-left {
  position: absolute;
  width: 3px;
  border-top: 3px solid rgba(0, 209, 182, 0.6);
  bottom: 0;
  left: 0px;
}

.corner-bottom-left::before {
  position: absolute;
  content: '';
  width: 3px;
  border-top: 3px solid rgba(0, 209, 182, 0.35);
  bottom: 0px;
  left: -3px;
}

.corner-bottom-right {
  position: absolute;
  width: 3px;
  border-top: 3px solid rgba(0, 209, 182, 0.6);
  bottom: 0;
  right: 0px;
}

.corner-bottom-right::before {
  position: absolute;
  content: '';
  width: 3px;
  border-top: 3px solid rgba(0, 209, 182, 0.35);
  bottom: 0;
  right: -3px;
}
</style>
