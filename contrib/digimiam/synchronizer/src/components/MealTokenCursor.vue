<template>
  <div 
    class="cursor"
    @mousedown="mousedown"
    :style="{top: top, left: left, zIndex: zIndex, height: height, width: width}"
  ></div>
</template>

<script>
import MenuStore from '@/store/MenuStore.js'

export default {
  name: 'MealTokenCursor',
  computed: {
    top: function() {
      return this.token.cursorTop + 'px'
    },
    left: function() {
      return this.token.cursorLeft + 'px'
    },
    zIndex: function() {
      return this.token.zIndex
    },
    width: function() {
      return this.token.cursorWidth + 'px'
    },
    height: function() {
      return this.token.cursorHeight + 'px'
    },
    token: function() {
      return MenuStore.state.tokens[this.tokenIndex]
    },
  },
  methods: {
    mousedown: function() {
      MenuStore.commit('tokenMousedown', this.tokenIndex)
    },
  },
  props: ['tokenIndex'],
}
</script>

<style scoped>
.cursor {
  position: absolute;
  background-color: white;
  border-radius: 50%;
}
</style>