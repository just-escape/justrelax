<template>
  <div class="position-relative h-100 w-100">
    <div
      class="window-container position-relative h-100"
      :class="{
        warning: theme === 'warning',
        danger: theme === 'danger',
      }"
    >
      <div
        class="window-frame"
        :class="{
          warning: theme === 'warning',
          danger: theme === 'danger',
        }"
      />
      <div
        class="window-title-ribbon mb-2 text-right p-2"
        :class="{
          warning: theme === 'warning',
          danger: theme === 'danger',
        }"
      >
        {{ title }}
      </div>

      <slot></slot>
    </div>
  </div>
</template>

<script>
export default {
  name: "Window",
  props: {
    title: {
      type: String,
      default: "TITLE",
    },
    theme: {
      type: String,
      default: "standard",
    },
  },
}
</script>

<style scoped>
.window-container {
  border: 1px solid transparent;
  border-top: 9px solid transparent;
  padding-top: 40px;
}

.window-frame {
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
  z-index: 1;
}

.window-frame.warning {
  filter: drop-shadow(1px 1px 4px rgba(255, 69, 0, 0.75));
}

.window-frame.danger {
  filter: drop-shadow(1px 1px 4px rgba(230, 0, 40, 1));
}

.window-frame::before {
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

.window-frame.warning::before {
  background-color: orangered;
}

.window-frame.danger::before {
  background-color: rgb(230, 0, 40);
}

.window-title-ribbon {
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

.window-title-ribbon.warning {
  border-bottom: 1px solid orangered;
  background-color: rgba(0, 0, 0, 1);
}

.window-title-ribbon.danger {
  border-bottom: 1px solid rgb(230, 0, 40);
  background-color: rgba(0, 0, 0, 1);
}
</style>