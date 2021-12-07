<template>
  <i class='fas fa-chevron-down pointer' :class="{'fa-lg': size == 'fa-lg'}"></i>
</template>

<script>
export default {
  name: 'CollapseChevron',
  props: {
    size: {
      type: String,
      default: "fa-lg",
    }
  }
}
</script>

<style scoped>
i {
  transition: transform 0.2s ease-in-out;
}

.collapsed {
  transform: rotate(-90deg);
}
</style>
