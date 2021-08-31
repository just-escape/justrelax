<template>
  <div
    class="position-absolute badge text-left"
    style="right: 0px; font-size: 14px; border: 1px solid rgba(0, 209, 182, 0.7); font-weight: normal"
    :style="{
      opacity: notifOpacity,
      bottom: notifBottom + 'px',
      'border-color': theme === 'danger' ? 'rgba(253, 126, 20, 1)' : 'rgba(0, 209, 182, 0.7)',
      background: theme === 'danger' ? 'rgba(0, 0, 0, 0.8)' : 'rgba(0, 45, 80, 1)',
      color: theme === 'danger' ? 'rgb(253, 126, 20)' : 'rgb(0, 209, 182)',
    }"
    v-html="message"
  >
  </div>
</template>

<script>
export default {
  name: "BadgeNotification",
  data() {
    return {
      notifOpacity: 1,
      notifBottom: 0,
    }
  },
  mounted() {
    this.$anime({
      targets: this,
      notifBottom: 60,
      notifOpacity: 0,
      duration: this.fadeDelay,
      easing: 'easeInQuad',
    })
  },
  props: {
    message: String,
    fadeDelay: Number,
    theme: {
      type: String,
      default: 'blue',
    },
  },
}
</script>
