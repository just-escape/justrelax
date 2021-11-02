<template>
  <div
    class="alarm-window z-index-20 position-absolute"
    :style="{top: top, left: left, transform: transform}"
  >
    <Window :title="$t('danger')" theme="danger">
      <div class="d-flex flex-column h-100 justify-content-center align-items-center bg-black-09-transparent">
        <div class="d-flex flex-column align-items-center">
          <i class="text-red fa fa-exclamation-triangle mb-4 text-big" :style="{opacity: opacity}"/>
          <div style="font-size: 50px">
            Instrusion détectée
          </div>
          <div style="font-size: 40px">
            Évacuation <span class="text-red" style="font-weight: bold">complète</span> de la salle requise
          </div>
        </div>
      </div>
    </Window>
  </div>
</template>

<script>
import Window from '@/components/Window.vue'
import businessStore from '@/store/businessStore.js'

export default {
  name: "AlarmWindow",
  components: {
    Window,
  },
  data() {
    return {
      topOffset: 180,
      leftOffset: 420,
      scaleX: 0,
      scaleY: 0,
      opacity: 1,
    }
  },
  computed: {
    top() {
      return "calc(0px + " + this.topOffset + "px)"
    },
    left() {
      return "calc(0px + " + this.leftOffset + "px)"
    },
    transform() {
      return "scaleX(" + this.scaleX + ") scaleY(" + this.scaleY + ")"
    },
    displayed() {
      return businessStore.state.displayAlarmWindow
    },
  },
  methods: {
    blink() {
      this.$anime({
        targets: this,
        opacity: 0,
        duration: 1,
        delay: 100,
        endDelay: 150,
        loop: true,
        direction: 'alternate',
        easing: 'easeInQuad',
      })
    },
  },
  watch: {
    displayed(newValue) {
      if (newValue) {
        this.$anime({
          targets: this,
          scaleX: 1,
          scaleY: 1,
          duration: 400,
          easing: 'easeInQuad',
        })

        setTimeout(this.blink, 400)
      } else {
        this.$anime({
          targets: this,
          scaleX: 0,
          scaleY: 0,
          duration: 700,
          easing: 'easeInOutQuad',
        })
      }
    },
  }
}
</script>

<style scoped>
.alarm-window {
  width: 1080px;
  height: 720px;
}
</style>