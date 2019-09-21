<template>
  <div class="d-flex flex-row justify-content-around">
    <Widget
      v-for="m in measures"
      :key="m.id"
      :data="m"
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
          name: 'Temp.',
          label: 'ok',
          icon: ['fas', 'fa-thermometer-quarter'],
          gauge: 0.37,
          shadowAngle: 50,
          shadowCycle: 7000,
          error: false,
        },
        {
          name: 'Humidity',
          label: 'ok',
          icon: ['fas', 'fa-tint'],
          gauge: 0.18,
          shadowAngle: 200,
          shadowCycle: 3800,
          error: false,
        },
        {
          name: 'Stocks',
          label: 'error',
          icon: ['fas', 'fa-tags'],
          gauge: 0.89,
          shadowAngle: 100,
          shadowCycle: 5000,
          error: true,
        },
      ]
    }
  },
}
</script>
