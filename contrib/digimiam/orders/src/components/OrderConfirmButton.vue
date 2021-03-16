<template>
  <b-btn
    @click="click"
    class="font-weight-bold custom-transition py-3"
    block
    :size="size"
    :variant="gray ? 'secondary' : 'info'"
    :disabled="disabled"
    :style="{'boxShadow': boxShadow}"
  >
    <slot></slot>
  </b-btn>
</template>

<script>
export default {
  name: "PulsatingPrimaryButton",
  data() {
    return {
      boxShadowRadius: 0,
      boxOpacity: 0.5,
      animation: null,
    }
  },
  computed: {
    boxShadow: function() {
      return '0 0 0 ' + this.boxShadowRadius + 'px rgba(23, 162, 184, ' + this.boxOpacity + ') !important'
    },
  },
  methods: {
    click: function() {
      if (!this.disabled) {
        this.$emit('click')
      }
    },
  },
  watch: {
    pulse: function(newValue) {
      if (newValue) {
        this.animation.play()
      }
    }
  },
  mounted() {
    let this_ = this
    this.animation = this.$anime.timeline({
      targets: this_,
      loop: true,
      loopComplete: function() {
        this_.boxShadowRadius = 0
        this_.boxOpacity = 0.5
        if (!this_.pulse) {
          this_.animation.pause()
        }
      },
    })
    .add({
      boxShadowRadius: 30,
      duration: 1500,
      easing: 'easeOutQuart',
    })
    .add({
      boxOpacity: 0,
      duration: 1500,
      easing: 'easeOutSine',
      endDelay: 1000,
    }, '-=1500')
  },
  props: ["size", "pulse", "disabled", "gray"]
}
</script>

<style scoped>
/* bootstrap value except for the box-shadow that prevents the animejs animation to be displayed */
.custom-transition {
  transition: color 0.15s ease-in-out, background-color 0.15s ease-in-out, border-color 0.15s ease-in-out;
}

button:disabled {
  opacity: 0.4;
}
</style>
