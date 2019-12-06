<template>
  <div class="row background-image"></div>
</template>

<script>
export default {
  name: "Header",
}
</script>

<style scoped>
.background-image {
  height: 200px;
  background-image: url("~@/assets/rawfood.webp");
  background-position: 0px -200px;
  background-size: cover;
}
</style>
