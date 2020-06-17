<template>
  <Window :title="$t('INTELLIGENCE CULINAIRE')" class="oveflow-hidden">
    <video src="@/assets/marmitron_background.mp4" autoplay loop class="position-absolute"/>
    <video src="@/assets/marmitron.webm" autoplay loop class="position-absolute"/>
  </Window>
</template>

<script>
import Window from '@/components/Window.vue'

export default {
  name: "MarmitronWindow",
  components: {
    Window,
  },
}
</script>