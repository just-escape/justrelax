<template>
  <div class="position-relative d-inline-block" @mousedown="mousedown" @touchstart="mousedown">
    <div
      :style="{
        transform: 'scale(' + scale + ')',
      }"
      :class="{
        'frame-orange': color === 'orange',
        'text-orange': color === 'orange',
        'frame-teal': color === 'teal',
        'text-light': color === 'teal',
      }"
    >
      <div
        class="pb-3 pt-2_75 px-4_5"
        :class="{
          'bg-orange': color === 'orange' && fill,
          'bg-teal': color === 'teal' && fill,
        }"
      >
      {{ label }}
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "FramedButton",
  data() {
    return {
      scale: 1,
    }
  },
  methods: {
    mousedown() {
      this.$emit('mousedown')
      this.$anime.timeline({
        targets: this,
        easing: 'easeOutCubic',
        duration: 200,
      })
      .add({
        scale: 1.05,
      })
      .add({
        scale: 1,
      })
    },
  },
  props: {
    label: String,
    fill: {
      type: Boolean,
      default: false,
    },
    color: {
      type: String,
      default: "teal",
    },
  },
}
</script>

<style scoped>
.frame-teal {
  filter: drop-shadow(0 0 10px rgba(0, 209, 182, 0.4));
}

.frame-orange {
  filter: drop-shadow(0 0 10px rgba(253, 126, 20, 0.65));
}

.bg-teal {
  background: rgba(0, 209, 182);
  clip-path: polygon(
    14px 0%,
    calc(100% - 14px) 0%,
    100% 14px,
    100% calc(100% - 14px),
    calc(100% - 14px) 100%,
    14px 100%,
    0% calc(100% - 14px),
    0% 14px
  );
}

.bg-orange {
  background: rgba(253, 126, 20, 1);
  color: #03181f;
  clip-path: polygon(
    14px 0%,
    calc(100% - 14px) 0%,
    100% 14px,
    100% calc(100% - 14px),
    calc(100% - 14px) 100%,
    14px 100%,
    0% calc(100% - 14px),
    0% 14px
  );
}

.frame-teal::before {
  content: '';
  position: absolute;
  left: 0;
  top: 0;
  right: 0;
  bottom: 0;
  background-color: #00d1b6;
  clip-path: polygon(
    14px 0%,
    calc(100% - 14px) 0%,
    100% 14px,
    100% calc(100% - 14px),
    calc(100% - 14px) 100%,
    14px 100%,
    0% calc(100% - 14px),
    0% 14px,
    14px 0%,
    calc(14px + 7px) 3px,
    7px calc(14px + 3px),
    7px calc(100% - 14px - 3px),
    calc(14px + 3px) calc(100% - 7px),
    calc(100% - 14px - 3px) calc(100% - 7px),
    calc(100% - 7px) calc(100% - 14px - 3px),
    calc(100% - 7px) calc(14px + 3px),
    calc(100% - 14px - 3px) 7px,
    calc(14px + 3px) 7px
  );
  z-index: 10;
}

.frame-orange::before {
  content: '';
  position: absolute;
  left: 0;
  top: 0;
  right: 0;
  bottom: 0;
  background-color: var(--orange);
  clip-path: polygon(
    14px 0%,
    calc(100% - 14px) 0%,
    100% 14px,
    100% calc(100% - 14px),
    calc(100% - 14px) 100%,
    14px 100%,
    0% calc(100% - 14px),
    0% 14px,
    14px 0%,
    calc(14px + 7px) 3px,
    7px calc(14px + 3px),
    7px calc(100% - 14px - 3px),
    calc(14px + 3px) calc(100% - 7px),
    calc(100% - 14px - 3px) calc(100% - 7px),
    calc(100% - 7px) calc(100% - 14px - 3px),
    calc(100% - 7px) calc(14px + 3px),
    calc(100% - 14px - 3px) 7px,
    calc(14px + 3px) 7px
  );
  z-index: 10;
}

.pt-2_75 {
  padding-top: 1.2rem;
}

.px-4_5 {
  padding-left: 1.75rem;
  padding-right: 1.75rem;
}
</style>