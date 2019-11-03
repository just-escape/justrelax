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
  },
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
  color: orangered;
  position: relative;
  display: block;
  user-select: none;
}

.text-orange {
  color: orangered;
}

.glowing-container {
  border: 1px solid #ffc107;
  box-shadow: 0px 0px 14px -6px rgba(255, 193, 7, 1);
}

.global-container {
  height: 950px;
  width: 1200px;
}
</style>
