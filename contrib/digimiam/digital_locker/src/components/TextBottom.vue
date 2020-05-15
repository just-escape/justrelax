<template>
  <div class="position-relative">
    <div class="text">
      <i class="fas fa-exclamation-triangle"/> {{ $t('high_security_access') }}
    </div>
  </div>
</template>

<script>
export default {
  name: 'TextBottom'
}
</script>

<style scoped>
.text {
  padding: 0.6rem 1rem 0.5rem 1rem;
  color: orangered;
  background-color: rgba(00, 45, 80, 0.6);
  font-size: 20px;
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

.text::before {
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
    calc(10px + 1.5px) 1px,
    1.5px calc(10px + 1px),
    1.5px calc(100% - 10px - 1px),
    calc(10px + 1px) calc(100% - 1.5px),
    calc(100% - 10px - 1px) calc(100% - 1.5px),
    calc(100% - 1.5px) calc(100% - 10px - 1px),
    calc(100% - 1.5px) calc(10px + 1px),
    calc(100% - 10px - 1px) 1.5px,
    calc(10px + 1px) 1.5px
  );
  z-index: 10;
}
</style>