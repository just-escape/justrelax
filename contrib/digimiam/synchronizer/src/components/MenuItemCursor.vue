<template>
  <div
    class="cursor"
    :style="{top: cursorTop + 'px', opacity: opacity}"
  />
</template>

<script>
import menuStore from '@/store/menuStore.js'

export default {
  name: "MenuItemCursor",
  data() {
    return {
      cursorTop: 3,
      opacity: 1,
    }
  },
  computed: {
    cursorPosition() {
      return menuStore.state.cursorPosition
    },
    success() {
      return menuStore.state.success
    },
  },
  watch: {
    cursorPosition(newValue) {
      this.$anime({
        targets: this,
        cursorTop: 3 + 51 * newValue,
        duration: 1000,
        easing: 'easeOutQuint',
      })
    },
    success() {
      this.$anime({
        targets: this,
        opacity: 0,
        duration: 4000,
        easing: 'easeOutQuint',
      })
    },
  },
}
</script>

<style scoped>
.cursor {
  line-height: 27px;
  height: 17px;
  width: 14px;
  background-color: #00d1f6;
  left: 1px;
  clip-path: polygon(
    0% 0%,
    2px 0%,
    100% calc(50% - 1px),
    100% calc(50% + 1px),
    2px 100%,
    0% 100%
  );
}
</style>