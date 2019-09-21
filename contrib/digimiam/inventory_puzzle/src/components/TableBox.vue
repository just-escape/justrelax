<template>
  <div class="box position-relative">
    <div class="inner-border">
      <img class="img-fluid" src="@/assets/img/apple.png">
      <div class="text-center">
        <span class="text-teal">Name: </span><span class="text-white">{{ name }}</span>
      </div>
      <div class="text-center">
        <span class="text-teal">Weight: </span><span class="text-white">10kg</span>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'TableBox',
  props: ['name'],
}
</script>

<style scoped>
.box {
  padding: 10px;
}

.box::before {
  top: 10px;
  left: 10px;
  position: absolute;
  content: '';
  display: block;
  border: 12px solid #00d1b6;
  border-bottom-color: transparent;
  border-right-color: transparent;
}

.inner-border {
  border: 3px solid #00d1b6;
  padding: 5px;
  box-shadow: 0px 0px 14px -6px rgba(0, 209, 182, 0.75);
}

.box::after {
  position: absolute;
  content: '';
  bottom: 10px;
  right: 10px;
  height: 20px;
  width: 20px;
  border-bottom: 7px solid #00d1b6;
  border-right: 7px solid #00d1b6;
}

img {
  pointer-events: none;
}
</style>
