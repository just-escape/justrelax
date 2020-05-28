<template>
  <div
    class="position-absolute"
    :style="{
      left: dashLeft,
      bottom: dashBottom,
    }"
  >
    <div class="dash"
      :style="{
        width: dashWidth,
        height: dashHeight,
      }"
    />
    <i
      v-if="iconFa"
      class="position-absolute fa-fw"
      :class="icon"
      :style="{
        left: iconLeft,
        bottom: iconBottom,
        opacity: '0.7',
      }"
    />
    <img
      v-else
      :src="icon"
      class="position-absolute"
      :style="{
        left: iconLeft,
        bottom: iconBottom,
        opacity: '0.7',
      }"
      height="16px"
    />
  </div>
</template>

<script>
export default {
  name: "DishMatrixGraduation",
  props: {
    dashLeft: String,
    dashBottom: String,
    dashWidth: String,
    dashHeight: String,
    icon: String,
    iconFa: Boolean,
    iconLeft: String,
    iconBottom: String,
  },
}
</script>

<style scoped>
.dash {
  background-color: #00d1b6;
  box-shadow: 0px 1px 3px 0.01px rgba(0, 209, 182, 0.7);
}
</style>