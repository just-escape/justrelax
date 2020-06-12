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
  background: radial-gradient(ellipse at center, #03181f, rgb(3, 26, 34));
  position: relative;
  display: block;
  -webkit-user-select: none;
  -khtml-user-select: none;
  -moz-user-select: none;
  -ms-user-select: none;
  -o-user-select: none;
  user-select: none;
  color: var(--light);
}

.text-teal {
  color: #00d1b6;
}

.glowing-container {
  border: 1px solid #00d1b6;
  box-shadow: 0px 0px 14px -6px rgba(0, 209, 182, 1);
}

.transition-1s {
  transition: all 1s;
}
</style>
