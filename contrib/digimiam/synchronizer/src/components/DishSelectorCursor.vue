<template>
  <div 
    class="cursor"
    @mousedown="cursorPress"
    @touchstart="cursorPress"
    :style="{top: top, left: left, zIndex: zIndex, height: height, width: width}"
  >
    <div class="edge"></div>
    <div class="edge flip-vertically"></div>
    <div class="edge flip-horizontally"></div>
    <div class="edge flip-centrally"></div>
  </div>
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
  clip-path: polygon(
    30% 0%,
    70% 0%,
    100% 30%,
    100% 70%,
    70% 100%,
    30% 100%,
    0% 70%,
    0% 30%
  );
}

.edge {
  position: absolute;
  background-color: #00d1b6;
  top: 0;
  bottom: 0;
  right: 0;
  left: 0;
  clip-path: polygon(
    30% 0%,
    30% 4px,
    4px 30%,
    0% 30%
  );
}

.flip-vertically {
  transform: scaleX(-1);
}

.flip-horizontally {
  transform: scaleY(-1);
}

.flip-centrally {
  transform: scaleX(-1) scaleY(-1);
}
</style>