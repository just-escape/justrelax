<template>
  <div class="position-relative">
    <div class="position-absolute price bg-info rounded">10 nF</div>
    <img src="@/assets/gaufresque.png" class="img-fluid">
  </div>
</template>

<script>
export default {
  name: "OrderSummaryItem",
}
</script>

<style scoped>
.price {
  bottom: 10px;
  right: 8px;
  color: white;
  opacity: 0.85;
  filter: drop-shadow(0px 0px 4px rgba(23, 162, 184, 0.75));
  font-size: 0.8rem;
  padding: 1px 5px;
}
</style>
