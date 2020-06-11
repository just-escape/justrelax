<template>
  <Window :title="$t('INTELLIGENCE CULINAIRE')" class="overflow-hidden">
    <video src="@/assets/Wireframe.mp4" loop class="h-100 position-absolute" style="left: -45%"></video>
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