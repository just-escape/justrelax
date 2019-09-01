<template>
  <div class="p-3 h-75px text-center justify-content-center position-relative d-flex">
    <a href="/" class="align-self-center">
      <h1 class="big-noodle oblique">
        Just
        <img style="height: 50px" alt="Just Relax logo" src="@/assets/logo.png">
        Relax
      </h1>
    </a>
    <div class="position-absolute big-noodle oblique take-it-easy small">Take it easy</div>
  </div>
</template>

<script>
export default {
  name: 'AppNavBrand'
}
</script>

<style scoped>
.take-it-easy {
  bottom: 4px;
  right: 30px;
}
</style>
