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
  color: var(--light);
  position: relative;
  display: block;
  user-select: none;
  background: radial-gradient(ellipse at center, #03181f, rgb(3, 26, 34));
}

.text-orange {
  color: orangered;
}

.text-teal {
  color: #00d1b6;
}

.size-50 {
  font-size: 52px;
}

.lh-1 {
  line-height: 1;
}

.glowing-container {
  border: 1px solid #00d1b6;
  box-shadow: 0px 0px 14px -6px rgba(0, 209, 182, 1);
}

button:hover {
  background: transparent;
}

.btn-outline-info:not(:disabled):not(.disabled):focus {
  background: transparent;
}

.bottom-right {
  bottom: 5px;
  right: 5px;
}

.upper-top-right {
  bottom: calc(-26px - 5px);
  right: 0px;
}

video {
  display: block;
}

.video-thumbnail {
   width: 160px;
   height: 90px;
}

.size-20 {
  font-size: 20px;
}

.top-left {
  top: 0;
  bottom: 0;
}

.svg-glowing {
  filter: drop-shadow(0px 0px 3px #00d1b6);
}
</style>
