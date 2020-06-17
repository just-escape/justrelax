<template>
  <div>
    <Window :title="$t('alimentary_statistics')">
      <div class="d-flex flex-column align-items-center mt-2">
        <Widgets class="mt-1 mb-4"/>
        <Charts class="mb-4"/>
        <Bars/>
      </div>
    </Window>
  </div>
</template>

<script>
import Window from '@/components/Window.vue'
import Widgets from '@/components/Widgets.vue'
import Charts from '@/components/Charts.vue'
import Bars from '@/components/Bars.vue'

export default {
  name: "DecorationPanel",
  components: {
    Window,
    Widgets,
    Charts,
    Bars,
  },
}
</script>