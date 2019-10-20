<template>
  <div class="d-flex flex-column position-relative">
    <div
      :class="{'error': data.error}"
      class="round-box position-relative m-2"
    >
      <div
        class="shadowed-round-box"
        :style="{transform: 'rotate(' + shadowAngle + 'deg)'}"
      ></div>
      <WidgetGauge :fill="data.gauge" :anime="data.anime"/>
      <div class="h-100 box-content d-flex flex-column text-center justify-content-center pt-2">
        <i :class="data.icon" class="mb-1"></i>
        <span>{{ data.label }}</span>
      </div>
    </div>
    <div class="box-label text-center">
      {{ data.name }}
    </div>
  </div>
</template>

<script>
import WidgetGauge from '@/components/WidgetGauge.vue'

export default {
  name: 'Widget',
  data: function() {
    return {
      shadowAngle: 0
    }
  },
  components: {
    WidgetGauge,
  },
  mounted: function() {
    this.shadowAngle = this.data.shadowAngle

    this.$anime({
      targets: this,
      shadowAngle: 360 + this.data.shadowAngle,
      duration: this.data.shadowCycle,
      loop: true,
      easing: 'linear',
    })
  },
  props: ['data'],
}
</script>

<style scoped>
.round-box {
  border-radius: 50%;
  border: 2px solid #00d1b8;
  height: 72px;
  width: 72px;
  flex-grow: 1;
  color: #00d1b8;
  font-size: 12px;
  background-color: #01222f;
}

.shadowed-round-box {
  position: absolute;
  border-radius: 50%;
  height: 100%;
  width: 100%;
  box-shadow: 4px 0px 6px 0px rgba(0, 209, 182, 0.75);
}

.box-label {
  font-size: 12px;
  line-height: 1;
}

.error.round-box {
  color: orangered;
  border: 2px solid orangered;
}

.error .shadowed-round-box {
  border-radius: 50%;
  box-shadow: 4px 0px 6px 0px rgba(255, 69, 00, 0.75);
}

i {
  font-size: 26px;
}

.box-content > i, .box-content > span {
  z-index: 10;
}
</style>