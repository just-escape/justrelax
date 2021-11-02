<template>
  <div
    class="alarm-window z-index-20 position-absolute"
    :style="{top: top, left: left, display: displayed ? 'block' : 'none'}"
  >
    <Window :title="$t('alarm')" theme="danger" style="color: var(--light)">
      <div class="d-flex flex-column h-100 justify-content-center align-items-center bg-black-transparent">
        <div class="d-flex flex-column align-items-center">
          <i class="text-red fa fa-exclamation-triangle mb-4 blink" style="font-size: 300px"/>
          <div style="font-size: 40px; color: var(--light)">
            Instrusion détectée
          </div>
          <div style="font-size: 24px; color: var(--light)">
            Évacuation <span class="text-red" style="font-weight: bold">complète</span> de la salle requise
          </div>
        </div>
      </div>
    </Window>
  </div>
</template>

<script>
import Window from '@/components/Window.vue'
import lockStore from '@/store/lockStore.js'

export default {
  name: "AlarmWindow",
  components: {
    Window,
  },
  data() {
    return {
      topOffset: 180,
      leftOffset: 20,
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
      return lockStore.state.displayAlarmWindow
    },
  },
}
</script>

<style scoped>
.alarm-window {
  width: 560px;
  height: 664px;
}

@keyframes blink {
	0% { opacity: 0 }
	49% { opacity: 0 }
	50% { opacity: 1 }
}

.blink {
  animation: blink 1s infinite
}

.bg-black-transparent {
  background-color: rgba(0, 0, 0, 0.9);
}

.text-red {
  color: rgb(230, 0, 40);
}
</style>