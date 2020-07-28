<template>
  <div class="menu position-relative">
    <div
      class="position-absolute video-placeholder"
    />
    <div
      class="position-absolute pt-4 mt-5 w-100 pl-center position-absolute text-xl text-orange drop-shadow-orange text-las-enter"
    >{{ $t('meals') }}</div>
    <div class="frame"/>
  </div>
</template>

<script>
export default {
  name: "MenuFrame"
};
</script>

<style scoped>
.menu {
  width: 980px;
  height: 1360px;
  display: block; /* Removes a mysterious margin bottom */
}

.frame {
  width: 980px;
  height: 1360px;
  display: block; /* Removes a mysterious margin bottom */
  filter: drop-shadow(0 0 10px rgba(0, 209, 182, 0.4));
}

.frame::before {
  content: "";
  position: absolute;
  left: 0;
  top: 0;
  right: 0;
  bottom: 0;
  background-color: #00d1b6;
  clip-path: polygon(
    30px 0%,
    calc(100% - 30px) 0%,
    100% 30px,
    100% calc(100% - 30px),
    calc(100% - 30px) 100%,
    30px 100%,
    0% calc(100% - 30px),
    0% 30px,
    30px 0%,
    calc(30px + 10px) 5px,
    10px calc(30px + 5px),
    10px calc(100% - 30px - 5px),
    calc(30px + 5px) calc(100% - 10px),
    calc(100% - 30px - 5px) calc(100% - 10px),
    calc(100% - 10px) calc(100% - 30px - 5px),
    calc(100% - 10px) calc(30px + 5px),
    calc(100% - 30px - 5px) 10px,
    calc(30px + 5px) 10px
  );
  z-index: 10;
}

.pl-center {
  padding-left: 270px;
}

.video-placeholder {
  background: var(--light);
  width: 900px;
  height: 1150px;
  top: 160px;
  left: 40px;
}
</style>