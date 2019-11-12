<template>
  <i class='fas fa-chevron-down fa-lg pointer'></i>
</template>

<script>
export default {
  name: 'CollapseChevron'
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
