<template>
  <div class="frame position-relative">
    <div class="h1-background-ribbon"></div>
    <div class="top-left-corner"></div>
    <div class="bottom-left-corner"></div>
    <div class="content d-flex flex-column">
      <h1 class="text-right mb-3">DIGIMIAM FOOD SUPPLIES</h1>
      <Widgets class="mb-3"/>
      <Logs/>
    </div>
  </div>
</template>

<script>
import Widgets from '@/components/Widgets.vue'
import Logs from '@/components/Logs.vue'

export default {
  name: 'LeftMenu',
  components: {
    Logs,
    Widgets,
  },
}
</script>

<style scoped>
.frame {
  padding: 5px;
  z-index: 20;
}

.content {
  border: 3px solid #00d1b6;
  border-top: 9px solid #00d1b6;
  box-shadow: 0px 0px 14px -6px rgba(0, 209, 182, 1);
  height: 100%; /*calc(100% - 50px + 13px);*/
  background-color: rgba(00, 45, 64, 0.5);
  padding: 10px;
  color: #ffffff;
}

.h1-background-ribbon {
  position: absolute;
  margin: 3px;
  top: 11px;
  background-color: rgba(00, 45, 64, 0.6);
  height: 34px;
  width: calc(100% - 6px - 10px);
  border-bottom: 1px solid #00d1b6;
}

.content h1 {
  font-size: 18px;
  color: #ffffff;
  z-index: 21;
}

.top-left-corner {
  position: absolute;
  top: 11px;
  left: 5px;
  display: block;
  border: 20px solid #00d1b6;
  border-bottom-color: transparent;
  border-right-color: transparent;
}

.bottom-left-corner {
  position: absolute;
  bottom: 5px;
  left: 5px;
  display: block;
  border: 20px solid #00d1b6;
  border-right-color: transparent;
  border-top-color: transparent;
}
</style>
