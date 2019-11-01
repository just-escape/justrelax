<template>
  <div
    id="app"
    v-touch:moving="moving"
    v-touch:end="tapEnd"
    @mouseleave="mouseleave"
    class="d-flex justify-content-center position-relative h-100"
  >
    <BackgroundLines/>
    <div class="padding-top-10px global-container row py-3">
      <div class="col-9">
        <div class="d-flex flex-column">
          <LightPuzzle class="h-402px mb-4"/>
          <MenuPuzzle class="h-492px"/>
        </div>
      </div>
      <div class="col-3">
        <Logs/>
      </div>
    </div>
  </div>
</template>

<script>
import BackgroundLines from '@/components/BackgroundLines.vue'
import LightPuzzle from '@/components/LightPuzzle.vue'
import MenuPuzzle from '@/components/MenuPuzzle.vue'
import Logs from '@/components/Logs.vue'
import MenuStore from '@/store/MenuStore.js'

export default {
  name: 'app',
  components: {
    BackgroundLines,
    Logs,
    LightPuzzle,
    MenuPuzzle,
  },
  methods: {
    moving: function(event) {
      MenuStore.commit('appMoving', event)
    },
    tapEnd: function() {
      MenuStore.commit('appTapEnd')
    },
    mouseleave: function() {
      MenuStore.commit('appMouseleave')
    },
  },
  mounted() {
    // Disable longtap (right click) menu to appear
    window.oncontextmenu = function() {
      return false;
    }
    this.$connect()
  }
}
</script>

<style>
@font-face {
    font-family: "Code New Roman";
    font-style: normal;
    src: url('./assets/webfonts/code-new-roman.woff2') format('woff2');
}

#app {
  font-family: 'Code New Roman', 'sans-serif';
  color: #ffffff;
  position: relative;
  display: block;
  -webkit-user-select: none;
  -khtml-user-select: none;
  -moz-user-select: none;
  -ms-user-select: none;
  -o-user-select: none;
  user-select: none;
}

.padding-top-10px {
  padding-top: 10px;
}

#app::before {
  content: "";
  background: radial-gradient(ellipse at center, #03181f, rgb(3, 26, 34));
  position: absolute;
  right: 0;
  bottom: 0;
  left: 0;
  top: 0;
  z-index: -1;
}

.text-teal {
  color: #00f6d1;
}

.text-orange {
  color: orangered;
}

.global-container {
  height: 950px;
  width: 1200px;
}

.glowing-container {
  border: 1px solid #00d1b6;
  box-shadow: 0px 0px 14px -6px rgba(0, 209, 182, 1);
}

.h-402px {
  height: 402px;
}

.h-492px {
  height: 492px;
}
</style>
