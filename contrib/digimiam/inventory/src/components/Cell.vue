<template>
  <div :style="{background: background}"></div>
</template>

<script>
export default {
  name: "Cell",
  computed: {
    background() {
      if (this.content === 'W') {
        return 'rgb(120, 120, 120)'
      } else if (this.content === '.') {
        return 'rgba(230, 230, 230, 0)'
      } else {
        return 'rgb(0, 0, 0)'
      }
    }
  },
  props: {
    content: String,
  }
}
</script>