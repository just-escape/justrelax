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
  font-family: "Gotham";
  font-style: normal;
  src: url('./assets/webfonts/gotham-book.woff') format('woff');
}

#app {
  font-family: 'Gotham', 'sans-serif';
  color: #222;
  background-color: wheat;
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

.text-white {
  color: var(--light);
}
</style>
