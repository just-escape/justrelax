<template>
  <div class="d-flex flex-column justify-content-between h-100">
    <div class="d-flex flex-column flex-grow-1 mb-4">
      <RowTop class="mb-3"/>
      <RowMiddle class="mb-3"/>
      <RowBottom/>
    </div>

    <LeftPanelButtons/>
  </div>
</template>

<script>
import RowTop from "@/components/RowTop.vue"
import RowMiddle from "@/components/RowMiddle.vue"
import RowBottom from "@/components/RowBottom.vue"
import LeftPanelButtons from '@/components/LeftPanelButtons.vue'

export default {
  name: "LeftPanel",
  components: {
    RowTop,
    RowMiddle,
    RowBottom,
    LeftPanelButtons,
  },
}
</script>
