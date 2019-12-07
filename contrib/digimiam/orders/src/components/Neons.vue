<template>
  <div class="position-relative h-100 flex-grow-1">
    <div class="position-absolute neon-left neon-top"></div>
    <div class="position-absolute neon neon-top"></div>
    <div class="position-absolute neon-right neon-top"></div>

    <div class="position-absolute neon-left neon-middle"></div>
    <div class="position-absolute neon neon-middle"></div>
    <div class="position-absolute neon-right neon-middle"></div>

    <div class="position-absolute neon-left neon-bottom"></div>
    <div class="position-absolute neon neon-bottom"></div>
    <div class="position-absolute neon-right neon-bottom"></div>
  </div>
</template>

<script>
export default {
  name: "Neons"
}
</script>

<style scoped>
/* A lot of repetition, sorry :| */

.neon {
  height: 3px;
  left: 10px;
  width: calc(100% - 20px);
  background-color: var(--primary);
  opacity: 0.75;
  box-shadow: 0px 0px 2px var(--primary);
}

.neon-left {
  height: 3px;
  width: 10px;
  background-color: var(--primary);
  opacity: 0.75;
  box-shadow: 0px 0px 2px var(--primary);
  border-top-left-radius: 50%;
  border-bottom-left-radius: 50%;
}

.neon-right {
  height: 3px;
  width: 10px;
  right: 0;
  background-color: var(--primary);
  opacity: 0.75;
  box-shadow: 0px 0px 2px var(--primary);
  border-top-right-radius: 50%;
  border-bottom-right-radius: 50%;
}

.neon-top {
  top: calc(25% - 2px);
}

.neon-middle {
  top: calc(50% - 2px);
}

.neon-bottom {
  top: calc(75% - 1px);
}
</style>
