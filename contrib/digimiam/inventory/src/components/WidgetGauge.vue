<template>
  <div>
    <div class="gauge"></div>
    <div
      class="gauge-indicator"
      :style="{transform: 'rotate(' + value + 'deg)'}"
    ></div>
    <div class="gauge-inner-mask"></div>
  </div>
</template>

<script>
export default {
  name: 'WidgetGauge',
  computed: {
    value: function() {
      return (1 - this.fill) * -180
    },
  },
  props: ['fill']
}
</script>

<style scoped>
.gauge {
  background: #00d1b8;
  position: absolute;
  border-radius: 50%;
  height: calc(100% - 4px);
  width: calc(100% - 4px);
  top: 2px;
  left: 2px;
  clip-path: polygon(50% 0%, 50% 100%, 100% 100%, 100% 0%);
}

.error .gauge {
  background-color: orangered;
}

.gauge-indicator {
  background: #01222f;
  position: absolute;
  border-radius: 50%;
  height: calc(100% - 1px);
  width: calc(100% - 1px);
  clip-path: polygon(0% 0%, 50% 0%, 50% 100%, 0% 100%);
}

.gauge-inner-mask {
  background: #01222f;
  position: absolute;
  border-radius: 50%;
  height: calc(100% - 4px - 4px);
  width: calc(100% - 4px - 4px);
  top: 4px;
  left: 4px;
}
</style>
