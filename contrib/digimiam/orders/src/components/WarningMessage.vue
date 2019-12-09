<template>
  <div class="d-flex justify-content-center align-items-center">
    <WarningWindow class="w-50 h-50"/>
  </div>
</template>

<script>
import WarningWindow from "@/components/WarningWindow.vue"

export default {
  name: "WarningMessage",
  components: {
    WarningWindow,
  },
}
</script>
