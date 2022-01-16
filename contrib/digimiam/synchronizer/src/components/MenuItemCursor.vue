<template>
  <div
    class="cursor"
    :style="{top: cursorTop + 'px', opacity: success ? 0 : 1}"
  />
</template>

<script>
import menuStore from '@/store/menuStore.js'

export default {
  name: "MenuItemCursor",
  computed: {
    cursorTop() {
      return 5 + 51 * menuStore.state.cursorPosition
    },
    success() {
      return menuStore.state.success
    },
  },
}
</script>

<style scoped>
.cursor {
  line-height: 27px;
  height: 15px;
  width: 13px;
  background-color: #00d1f6;
  left: 3px;
  clip-path: polygon(
    0% 0%,
    2px 0%,
    100% calc(50% - 1px),
    100% calc(50% + 1px),
    2px 100%,
    0% 100%,
    0% 3px,
    2.5px 3px,
    2.5px calc(100% - 3px),
    calc(100% - 3px) 50%,
    2.5px 3px,
    0% 3px
  );
  transition: top 1s ease-in-out, opacity 2s ease-in-out;
}
</style>