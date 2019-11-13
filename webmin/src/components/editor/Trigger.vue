<template>
  <div>
    <InlineSelect :options="options" :default="selected"/> - {{ trigger }}
  </div>
</template>

<script>
import InlineSelect from "@/components/common/InlineSelect.vue"

export default {
  name: "Trigger",
  components: {
    InlineSelect,
  },
  data() {
    return {
      options: [
        'Message received',
        'Message sent',
        'Timer expired',
        'Session tick',
        'Session started',
        'Session paused',
        'Session resumed',
      ],
      selected: 'Message received',
    }
  },
  props: {
    trigger: Object,
  }
}
</script>
