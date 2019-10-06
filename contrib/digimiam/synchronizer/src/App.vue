<template>
  <div id="app" class="d-flex justify-content-center h-100">
    <div class="global-container d-flex flex-column">
      <TopModules class="mt-3 mb-4"/>
      <MenuSelector/>
    </div>
  </div>
</template>

<script>
import TopModules from '@/components/TopModules.vue'
import MenuSelector from '@/components/MenuSelector.vue'

export default {
  name: 'app',
  components: {
    TopModules,
    MenuSelector,
  },
  mounted() {
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
  padding-top: 10px;
  position: relative;
  display: block;
  -webkit-user-select: none;
  -khtml-user-select: none;
  -moz-user-select: none;
  -ms-user-select: none;
  -o-user-select: none;
  user-select: none;
}

#app::before {
  content: "";
  background: url('./assets/img/background-grid.png');
  position: absolute;
  right: 0;
  bottom: 0;
  left: 0;
  top: 0;
  opacity: 0.3;
  z-index: -1;

}

#app::after {
  content: "";
  background-color: #03181f;
  position: absolute;
  right: 0;
  bottom: 0;
  left: 0;
  top: 0;
  z-index: -2;
}

.text-teal {
  color: #00f6d1;
}

.text-orange {
  color: orangered;
}

.global-container {
  height: 956px;
  width: 1206px;
  border: 3px solid #00d1b6;
}

.glowing-container {
  border: 1px solid #00d1b6;
  box-shadow: 0px 0px 14px -6px rgba(0, 209, 182, 1);
}
</style>
