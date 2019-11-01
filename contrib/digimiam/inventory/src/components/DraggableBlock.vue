<template>
  <div class="position-absolute">
    <div
      class="block position-absolute"
      @mousedown="mousedown"
      :style="{
        left: left + 'px',
        top: top + 'px',
        width: width + 'px',
        height: height + 'px',
        zIndex: zIndex,
      }"
    >
      <div
        class="inner-block"
        :style="{
          backgroundColor: color,
          'background-position': backgroundPosition,
          boxShadow: boxshadow
        }"
      ></div>
    </div>
  </div>
</template>

<script>
import store from '@/store/store.js'

export default {
  name: 'DraggableBlock',
  computed: {
    boxshadow: function() {
      return '0px 0px ' + this.shadowWidth + 'px -6px ' + this.color
    },
  },
  methods: {
    mousedown: function() {
      store.commit('blockMousedown', this.id)
    },
  },
  props: [
    "id",
    "left",
    "top",
    "width",
    "height",
    "color",
    "backgroundPosition",
    "zIndex",
    "shadowWidth",
  ]
}
</script>

<style scoped>
.block {
  margin-top: 3px;
  margin-left: 3px;
  padding: 1px;
}

.inner-block {
  width: 100%;
  height: 100%;
  border-radius: 4px;
  background-image: url('~@/assets/img/rust.png');
}
</style>
