<template>
  <div class="position-relative h-100 flex-grow-1">
    <div
      class="position-absolute neon-left neon-top"
      :style="{'box-shadow': boxShadow, background: color}"
    />
    <div
      class="position-absolute neon neon-top"
      :style="{'box-shadow': boxShadow, background: color}"
    />
    <div
      class="position-absolute neon-right neon-top"
      :style="{'box-shadow': boxShadow, background: color}"
    />

    <div
      class="position-absolute neon-left neon-middle"
      :style="{'box-shadow': boxShadow, background: color}"
    />
    <div
      class="position-absolute neon neon-middle"
      :style="{'box-shadow': boxShadow, background: color}"
    />
    <div
      class="position-absolute neon-right neon-middle"
      :style="{'box-shadow': boxShadow, background: color}"
    />

    <div
      class="position-absolute neon-left neon-bottom"
      :style="{'box-shadow': boxShadow, background: color}"
    />
    <div
      class="position-absolute neon neon-bottom"
      :style="{'box-shadow': boxShadow, background: color}"
    />
    <div
      class="position-absolute neon-right neon-bottom"
      :style="{'box-shadow': boxShadow, background: color}"
    />
  </div>
</template>

<script>
export default {
  name: "Neons",
  computed: {
    boxShadow() {
      return "0px 0px 2px " + this.color
    }
  },
  props: {
    color: {
      type: String,
      default: "var(--warning)",
    }
  },
}
</script>

<style scoped>
/* A lot of repetition, sorry :| */

.neon {
  height: 3px;
  left: 10px;
  width: calc(100% - 20px);
  opacity: 0.75;
}

.neon-left {
  height: 3px;
  width: 10px;
  opacity: 0.75;
  border-top-left-radius: 50%;
  border-bottom-left-radius: 50%;
}

.neon-right {
  height: 3px;
  width: 10px;
  right: 0;
  opacity: 0.75;
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
