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
    let ws_url = this.$route.query.ws_url
    if (ws_url) {
      this.$connect('ws://' + ws_url)
    } else {
      this.$connect('ws://localhost:3031')
    }
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

.transition-1s {
  transition: all 1s;
}

.text-orange {
  color: orangered;
}

.text-orange-light {
  color: #fd7e14;
}

.text-underline {
  text-decoration: underline;
}

.text-18 {
  font-size: 18px;
}

.text-big {
  font-size: 300px;
}

.z-index-20 {
  z-index: 20;
}

.input-warning {
  border: 1px solid #fd7e14;
  color: #fd7e14;
  height: 35px;
}

.text-teal {
  color: #00d1b6;
}

.text-red {
  color: rgb(230, 0, 40);
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

.password-window {
  width: 550px;
  height: 350px;
}

.bg-black-transparent {
  background-color: rgba(0, 0, 0, 0.8);
}

.bottom-right {
  bottom: 5px;
  right: 5px;
}

.upper-top-right {
  bottom: calc(-26px - 5px);
  right: 0px;
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

.btn-outline-info:focus {
  box-shadow: none;
}

video {
  display: block;
}

video:focus {
  outline: none !important;
}

.video-thumbnail {
   width: 160px;
   height: 90px;
}

video::-webkit-media-controls-fullscreen-button {
  display: none;
}

video::-webkit-media-controls-mute-button {
  display: none;
}

video::-webkit-media-controls-volume-slider {
  display: none;
}
</style>
