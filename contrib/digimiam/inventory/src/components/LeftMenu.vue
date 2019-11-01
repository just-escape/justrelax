<template>
  <div class="frame position-relative">
    <div class="h1-background-ribbon"></div>
    <div class="content d-flex flex-column">
      <h1 class="text-right mb-3">{{ $t("digimiam_food_stocks") }}</h1>
      <Widgets class="mb-3"/>
      <Charts class="mb-3"/>
      <Bars class="mb-3"/>
      <Logs/>
    </div>
  </div>
</template>

<script>
import Widgets from '@/components/Widgets.vue'
import Charts from '@/components/Charts.vue'
import Bars from '@/components/Bars.vue'
import Logs from '@/components/Logs.vue'

export default {
  name: 'LeftMenu',
  components: {
    Widgets,
    Charts,
    Bars,
    Logs,
  },
}
</script>

<style scoped>
.frame {
  padding: 5px;
  z-index: 20;
}

.content {
  border: 3px solid transparent;
  border-top: 9px solid transparent;
  height: 100%;
  padding: 10px;
  padding-bottom: 35px;
  color: #ffffff;
}

.h1-background-ribbon {
  position: absolute;
  margin: 3px;
  top: 11px;
  background-color: rgba(0, 45, 64, 0.6);
  height: 34px;
  width: calc(100% - 6px - 10px);
  border-bottom: 1px solid #00d1b6;
  clip-path: polygon(100% 0%, 100% 100%, -1px 100%, calc(40px - 4px) 0%);
}

.content h1 {
  font-size: 18px;
  color: #ffffff;
  z-index: 21;
}
</style>
