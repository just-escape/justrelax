<template>
  <div class="position-relative">
    <div class="title">
    {{ $t('server_room') }}
    </div>
  </div>
</template>

<script>
export default {
  name: 'Title',
}
</script>

<style scoped>
.title {
  padding: 0.8rem 3rem 0.5rem 3rem;
  color: white;
  background-color: rgba(00, 45, 80, 0.6);
  font-size: 50px;
  line-height: 1;
  clip-path: polygon(
    10px 0%,
    calc(100% - 10px) 0%,
    100% 10px,
    100% calc(100% - 10px),
    calc(100% - 10px) 100%,
    10px 100%,
    0% calc(100% - 10px),
    0% 10px
  );
}

.title::before {
  content: '';
  position: absolute;
  left: 0;
  top: 0;
  right: 0;
  bottom: 0;
  background-color: #00d1b6;
  clip-path: polygon(
    10px 0%,
    calc(100% - 10px) 0%,
    100% 10px,
    100% calc(100% - 10px),
    calc(100% - 10px) 100%,
    10px 100%,
    0% calc(100% - 10px),
    0% 10px,
    10px 0%,
    calc(10px + 5px) 3px,
    5px calc(10px + 3px),
    5px calc(100% - 10px - 3px),
    calc(10px + 3px) calc(100% - 5px),
    calc(100% - 10px - 3px) calc(100% - 5px),
    calc(100% - 5px) calc(100% - 10px - 3px),
    calc(100% - 5px) calc(10px + 3px),
    calc(100% - 10px - 3px) 5px,
    calc(10px + 3px) 5px
  );
  z-index: 10;
}
</style>