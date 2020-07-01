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

#app::before {
  content: "";
  background: rgb(3, 26, 34);
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

.glowing-container {
  border: 1px solid #00d1b6;
  box-shadow: 0px 0px 14px -6px rgba(0, 209, 182, 1);
}

.z-index-20 {
  z-index: 20;
}

.bg-black-transparent {
  background-color: rgba(0, 0, 0, 0.8);
}

.text-big {
  font-size: 300px;
}

.text-red {
  color: rgb(230, 0, 40);
}
</style>
