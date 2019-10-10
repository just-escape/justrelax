<template>
  <div class="h-100">
    <div class="d-flex flex-column justify-content-between h-100">
      <div class="flex-grow-1 mb-4 position-relative">
        <div class="glowing-wire top-wire"></div>
        <div class="glowing-wire bottom-wire"></div>

        <div class="h-100">
          <div class="menu-frame"></div>
          <div class="menu-background"></div>
          
          <div class="d-flex flex-row h-100">
            <div class="title-ribbon pb-2 pl-3 d-flex align-items-end">
              <div class="title">DEVICES SYNCHRONIZATION</div>
            </div>
            <LightPuzzleMenuContent class="h-100"/>
          </div>
        </div>
      </div>
      <div class="position-relative">
        <div class="glowing-wire center-wire"></div>

        <ButtonBlue class="lh-13">START MANUAL SYNCHRONIZATION</ButtonBlue>
      </div>
    </div>
  </div>
</template>

<script>
import LightPuzzleMenuContent from '@/components/LightPuzzleMenuContent.vue'
import ButtonBlue from '@/components/ButtonBlue.vue'

export default {
  name: 'LightPuzzleMenu',
  components: {
    LightPuzzleMenuContent,
    ButtonBlue,
  }
}
</script>

<style scoped>
.glowing-wire {
  position: absolute;
  /* 2 * bootstrap column padding */
  width: calc(2 * 15px);
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

.center-wire {
  top: 50%;
}

.lh-13 {
  line-height: 1.3;
}

.title-ribbon {
  background-color: rgba(00, 45, 64, 0.6);
  border-right: 1px solid #00d1b6;
  padding-right: 2px;
  height: 100%;
  width: 48px;
  clip-path: polygon(
    100% 0%,
    100% 100%,
    0% 100%,
    0% 36px,
    36px 0%
  );
}

.title {
  line-height: 1.3;
  font-size: 18px;
  width: 100%;
  writing-mode: tb-rl;
  transform: rotate(180deg);
}

.menu-frame {
  position: absolute;
  left: 0px;
  top: 0px;
  right: 0px;
  bottom: 0px;
  filter: drop-shadow(1px 1px 4px rgba(0, 209, 182, 0.75));
  clip-path: polygon(
    calc(100% + 10px) calc(0% - 10px),
    calc(100% + 10px) calc(100% + 10px),
    calc(0% - 10px) calc(100% + 10px),
    calc(0% - 10px) 36px,
    36px calc(0% - 10px),
    calc(100% - 1px) calc(0% - 10px),
    calc(100% - 1px) 1px,
    calc(36px + 9px - 3px) 1px,
    9px calc(36px),
    9px calc(100% - 1px),
    calc(100% - 1px) calc(100% - 1px),
    calc(100% - 1px) calc(0% - 10px)
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
    100% 0%,
    100% 100%,
    0% 100%,
    0% 36px,
    34px 0%,
    calc(100% - 1px) 0%,
    calc(100% - 1px) 1px,
    calc(36px + 9px - 3px) 1px,
    9px calc(36px),
    9px calc(100% - 1px),
    calc(100% - 1px) calc(100% - 1px),
    calc(100% - 1px) 0%
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
    0% 36px,
    36px 0%
  );
  z-index: -1;
}
</style>