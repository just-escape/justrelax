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
  height: 59px;
  width: 113px;
  background-color: #00d1f6;
  left: 3px;
  transition: top 1s ease-in-out, opacity 2s ease-in-out;
}
</style>