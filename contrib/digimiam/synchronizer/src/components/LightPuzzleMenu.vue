<template>
  <div class="h-100">
    <div class="d-flex flex-column justify-content-between h-100 px-3">
      <div class="flex-grow-1 position-relative menu-container">
        <div class="glowing-wire top-wire"></div>
        <div class="glowing-wire bottom-wire"></div>

        <div class="h-100">
          <div class="menu-frame"></div>
          <div class="menu-background"></div>

          <div class="title-ribbon p-2">
            <div class="title">{{ $t('digimiam_lights') }}</div>
          </div>
          <LightPuzzleMenuContent class="h-100"/>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import LightPuzzleMenuContent from '@/components/LightPuzzleMenuContent.vue'

export default {
  name: 'LightPuzzleMenu',
  components: {
    LightPuzzleMenuContent,
  }
}
</script>

<style scoped>
.glowing-wire {
  position: absolute;
  width: calc(2 * 15px + 16px);
  height: 1px;
  left: 100%;
  border-top: 1px solid #00d1b6;
  box-shadow: 0px 1px 3px 0.01px rgba(0, 209, 182, 0.7);
}

.top-wire {
  top: 30%;
}

.bottom-wire {
  bottom: 30%;
}

.lh-13 {
  line-height: 1.3;
}

.title-ribbon {
  position: absolute;
  width: 100%;
  height: 40px;
  top: 0;
  right: 0;
  border-bottom: 1px solid #00d1b6;
  background-color: rgba(00, 45, 64, 0.6);
  font-size: 20px;
  clip-path: polygon(
    100% 0%,
    100% 100%,
    0% 100%,
    0px calc(43px - 9px),
    43px 0px
  );
}

.title {
  line-height: 1.3;
  font-size: 20px;
  text-align: right;
  width: 100%;
}

.menu-container {
  border: 1px solid transparent;
  border-top: 9px solid transparent;
  padding-top: 60px;
}

.menu-frame {
  position: absolute;
  left: -1px;
  top: -9px;
  right: -1px;
  bottom: -1px;
  filter: drop-shadow(1px 1px 4px rgba(0, 209, 182, 0.75));
  clip-path: polygon(
    calc(100% - 1px) -10px,
    calc(100% + 10px) -10px,
    calc(100% + 10px) calc(100% + 10px),
    -10px calc(100% + 6px),
    -10px calc(48px - 7px - 6px),
    calc(48px + 2px - 6px) -10px,
    calc(100% - 1px) -10px,
    calc(100% - 1px) 9px,
    calc(48px + 1px) 9px,
    1px 48px,
    1px calc(100% - 1px),
    calc(100% - 1px) calc(100% - 1px)
  );
  z-index: 10;
}

.menu-frame::before {
  content: '';
  position: absolute;
  left: 0;
  top: 0;
  right: 0;
  bottom: 0;
  background-color: #00d1b6;
  clip-path: polygon(
    calc(100% - 1px) 0%,
    100% 0%,
    100% 100%,
    0% 100%,
    0% calc(48px - 7px),
    calc(48px + 2px) 0%,
    calc(100% - 1px) 0%,
    calc(100% - 1px) 9px,
    calc(48px + 1px) 9px,
    1px 48px,
    1px calc(100% - 1px),
    calc(100% - 1px) calc(100% - 1px)
  );
  z-index: 10;
}

.menu-background {
  position: absolute;
  background-color: rgba(00, 45, 64, 0.5);
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  clip-path: polygon(
    100% 0%,
    100% 100%,
    0% 100%,
    0px calc(43px - 6px),
    calc(43px + 6px) 0px
  );
  z-index: -1;
}
</style>