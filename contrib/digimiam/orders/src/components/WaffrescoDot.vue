<template>
  <div class="position-absolute" :style="{top: top + 'px', left: left + 'px'}">
    <div class="position-relative">
      <SvgHexagon class="hexagon"/>
    </div>
  </div>
</template>

<script>
import SvgHexagon from '@/components/SvgHexagon.vue'

export default {
  name: "Dot",
  components: {
    SvgHexagon
  },
  props: {
    top: Number,
    left: Number,
  },
}
</script>

<style scoped>
.hexagon {
  width: 30px;
  position: absolute;
  top: -15px;
  left: -15px;
}
</style>