<template>
  <div 
    class="cursor"
    v-touch:start="tapStart"
    :style="{top: top, left: left, zIndex: zIndex, height: height, width: width}"
  ></div>
</template>

<script>
import menuStore from '@/store/menuStore.js'

export default {
  name: 'DishSelectorCursor',
  computed: {
    top: function() {
      return this.item.cursorTop + 'px'
    },
    left: function() {
      return this.item.cursorLeft + 'px'
    },
    zIndex: function() {
      return this.item.selectorZIndex
    },
    width: function() {
      return this.item.cursorWidth + 'px'
    },
    height: function() {
      return this.item.cursorHeight + 'px'
    },
    item: function() {
      return menuStore.state.menuItems[this.itemIndex]
    },
  },
  methods: {
    tapStart: function() {
      menuStore.commit('appTapStart', this.itemIndex)
    },
  },
  props: ['itemIndex'],
}
</script>

<style scoped>
.cursor {
  position: absolute;
  background-color: white;
  border-radius: 50%;
}
</style>