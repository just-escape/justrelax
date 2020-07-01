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
  font-family: "Gotham";
  font-style: normal;
  src: url('./assets/webfonts/gotham-book.woff') format('woff');
}

@font-face {
  font-family: "Code New Roman";
  font-style: normal;
  src: url('./assets/webfonts/code-new-roman.woff2') format('woff2');
}

#app {
  font-family: 'Gotham', 'sans-serif';
  background-color: black;
  position: relative;
  display: block;
  user-select: none;
}

.text-teal {
  color: #00f6d1;
}

.text-orange {
  color: orangered;
}

button {
  box-shadow: none !important;
}

video {
  display: block; /* Removes a mysterious margin bottom */
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

.text-code-new-roman {
  font-family: 'Code New Roman';
}
</style>
