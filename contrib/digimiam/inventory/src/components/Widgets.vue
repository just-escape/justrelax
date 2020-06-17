<template>
  <div class="d-flex flex-row justify-content-between w-75">
    <Widget
      v-for="(m, mIndex) in measures"
      :key="mIndex"
      :top="m.top"
      :left="m.left"
      :status="m.status"
      :label="m.label"
      :icon="m.icon"
      :error="m.error"
      :style="{width: '100px'}"
    />
  </div>
</template>

<script>
import Widget from '@/components/Widget.vue'

export default {
  name: 'Widgets',
  components: {
    Widget,
  },
  data: function() {
    return {
      measures: [
        {
          top: 0,
          left: 100,
          icon: "fa fa-thermometer-quarter",
          label: "temperature",
          error: false,
        },
        {
          top: 0,
          left: 100,
          icon: "fa fa-tint",
          label: "humidity",
          error: false,
        },
        {
          top: 0,
          left: 100,
          icon: "fa fa-tags",
          label: "stocks",
          error: true,
        },
      ],
    }
  },
}
</script>
