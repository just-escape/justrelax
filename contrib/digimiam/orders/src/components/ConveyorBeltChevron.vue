<template>
  <i class="fas fa-angle-right" :style="{opacity: opacity}"></i>
</template>

<script>
export default {
  name: "ConveyorBeltChevron",
  data() {
    return {
      opacity: 1,
      animation: null,
    }
  },
  watch: {
    blink: function(newValue) {
      if (newValue) {
        this.animation.play()
      } else {
        this.animation.pause()
      }
    }
  },
  mounted() {
    this.animation = this.$anime({
      targets: this,
      opacity: 0.3,
      loop: true,
      easing: 'easeOutQuad',
      direction: 'alternate',
      autoplay: false,
      duration: 400,
      endDelay: 400,
    })
    if (this.blink) {
      this.animation.play()
    }
  },
  props: ["blink"]
}
</script>
