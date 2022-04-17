<template>
  <div 
    class="cursor d-flex flex-row justify-content-center align-items-center"
    @mousedown="cursorPress"
    @touchstart="cursorPress"
    :style="{
      top: top,
      left: left,
      zIndex: zIndex,
      height: height,
      width: width,
      filter: filter,
    }"
  >
    <div style="font-size: 18px; transform: translateY(2px)">
      Plat {{ id }}
    </div>
  </div>
</template>

<script>
import menuStore from '@/store/menuStore.js'

export default {
  name: 'DishSelectorCursor',
  computed: {
    filter: function() {
      if (menuStore.state.menuItems[this.itemIndex].isDishValidated) {
        return 'hue-rotate(-40deg) brightness(0.65) contrast(0.95)'
      } else {
        return ''
      }
    },
    top: function() {
      return this.item.cursorTop + 'px'
    },
    left: function() {
      return this.item.cursorLeft + 'px'
    },
    zIndex: function() {
      return menuStore.state.menuItems[this.itemIndex].isDishValidated ? this.item.selectorZIndex - 1 : this.item.selectorZIndex
    },
    width: function() {
      return this.item.cursorWidth + 'px'
    },
    height: function() {
      return this.item.cursorHeight + 'px'
    },
    id() {
      return this.item.id
    },
    item: function() {
      return menuStore.state.menuItems[this.itemIndex]
    },
  },
  methods: {
    cursorPress: function() {
      menuStore.commit('cursorPress', this.itemIndex)
    },
  },
  props: ['itemIndex'],
}
</script>

<style scoped>
.cursor {
  position: absolute;
  background-color: rgba(0, 45, 80, 0.8);
  transition: filter 2s ease-in-out;
  border: 3px solid rgba(0, 209, 182, 0.7);;
}
</style>