<template>
  <span
    :class="{
      pointer: editable,
      'text-jaffa': editable,
      'text-underline': editable,
      'text-double': lastEdited,
      'font-italic': !editable,
    }"
  >
    <span>{{ argument }}</span>
  </span>
</template>

<script>
export default {
  name: "Argument",
  props: ["argument", "editable", "lastEdited"],
}
</script>

<style scoped>
.text-double {
  text-decoration-style: double;
}
</style>