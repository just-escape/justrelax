<template>
  <div
    class="danger-window z-index-20 position-absolute"
    :style="{top: top, left: left, transform: transform}"
  >
    <Window :title="$t('danger')" class="text-light text-code-new-roman" theme="danger">
      <div class="d-flex flex-column h-100 justify-content-center align-items-center bg-black-transparent">
        <div class="d-flex flex-column align-items-center">
          <i class="text-red fa fa-biohazard mb-4 text-big" :style="{opacity: opacity}"/>
          <div style="font-size: 50px">
            {{ $t('toxic_air_detected') }}
          </div>
          <div style="font-size: 30px">
            {{ $t('immediate_evac') }}
          </div>
        </div>
      </div>
    </Window>
  </div>
</template>

<script>
import Window from '@/components/Window.vue'
import progressionStore from '@/store/progressionStore.js'

export default {
  name: "DangerWindow",
  components: {
    Window,
  },
  data() {
    return {
      topOffset: 420,
      leftOffset: 180,
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
      return progressionStore.state.displayDangerWindow
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
.danger-window {
  width: 720px;
  height: 1080px;
}
</style>