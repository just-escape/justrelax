<template>
  <div id="app" class="h-100">
    <router-view/>
  </div>
</template>

<script>
export default {
  name: 'app',
  mounted() {
    // Disable longtap (right click) menu to appear
    window.oncontextmenu = function() {
      return false
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
  padding-top: 10px;
  position: relative;
  display: block;
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

.glowing-container {
  border: 1px solid #00d1b6;
  box-shadow: 0px 0px 14px -6px rgba(0, 209, 182, 1);
}

.global-container {
  height: 950px;
  width: 1200px;
}
</style>
