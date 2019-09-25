<template>
  <div class="box position-relative">
    <div class="polygon-border"></div>
    <img class="img-fluid" src="@/assets/img/apple.png">
    <div class="text-center">
      <span class="text-teal">Name: </span><span class="text-white">{{ name }}</span>
    </div>
    <div class="text-center">
      <span class="text-teal">Weight: </span><span class="text-white">10kg</span>
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
  padding: 18px;
}

.polygon-border {
  position: absolute;
  top: 8px;
  right: 8px;
  bottom: 8px;
  left: 8px;
  filter: drop-shadow(0px 0px 2px rgba(0, 209, 182, 0.75));
  clip-path: polygon(
    calc(100% + 4px) calc(100% + 4px),
    calc(100% + 4px) calc(100% - 20px),
    calc(100% - 8px) calc(100% - 20px),
    calc(100% - 8px) calc(100% - 8px),
    calc(100% - 20px) calc(100% - 8px),
    calc(100% - 20px) calc(100% - 4px),
    4px calc(100% - 4px),
    4px 24px,
    24px 4px,
    calc(100% - 4px) 4px,
    calc(100% - 4px) calc(100% - 20px),
    calc(100% + 4px) calc(100% - 20px),
    calc(100% + 4px) -4px,
    calc(22px - 8px) -4px,
    -4px calc(22px - 8px),
    -4px calc(100% + 4px)
  );
}

.polygon-border::before {
  position: absolute;
  content: '';
  clip-path: polygon(
    100% 100%,
    100% calc(100% - 20px),
    calc(100% - 8px) calc(100% - 20px),
    calc(100% - 8px) calc(100% - 8px),
    calc(100% - 20px) calc(100% - 8px),
    calc(100% - 20px) calc(100% - 4px),
    4px calc(100% - 4px),
    4px 24px,
    24px 4px,
    calc(100% - 4px) 4px,
    calc(100% - 4px) calc(100% - 20px),
    100% calc(100% - 20px),
    100% 0%,
    22px 0%,
    0% 22px,
    0% 100%
  );
  background: #00d1b6;
  top: 0;
  right: 0;
  bottom: 0;
  left: 0;
}

img {
  pointer-events: none;
}
</style>
