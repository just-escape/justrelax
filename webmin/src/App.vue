<template>
  <div id="app" class="d-flex flex-row flex-grow-1">
    <AppNav class="flex-shrink-0"></AppNav>

    <router-view class="bgc-softdark flex-grow-1"></router-view>
  </div>
</template>

<script>
import AppNav from '@/components/AppNav.vue'
import roomStore from '@/store/roomStore.js'

export default {
  name: 'App',
  components: {AppNav},
  mounted() {
    roomStore.dispatch('fetchRooms')
    this.$connect()
  }
}
</script>

<style>
@font-face {
    font-family: "Big Noodle";
    font-style: normal;
    font-display: swap;
    src: url('./assets/font/big-noodle.eot');
    src:
      url('./assets/font/big-noodle.eot?#iefix') format('embedded-opentype'),
      url('./assets/font/big-noodle.woff2') format('woff2'),
      url('./assets/font/big-noodle.woff') format('woff'),
      url('./assets/font/big-noodle.ttf') format('truetype');
    unicode-range: U+000-5FF, U+20AC; /* Latin */
}

@font-face {
    font-family: "Big Noodle";
    font-style: oblique;
    font-display: swap;
    src: url('./assets/font/big-noodle-oblique.eot');
    src:
      url('./assets/font/big-noodle-oblique.eot?#iefix') format('embedded-opentype'),
      url('./assets/font/big-noodle-oblique.woff2') format('woff2'),
      url('./assets/font/big-noodle-oblique.woff') format('woff'),
      url('./assets/font/big-noodle-oblique.ttf') format('truetype');
    unicode-range: U+000-5FF; /* Latin */
}

@font-face {
    font-family: "Roboto";
    font-style: normal;
    font-weight: 400;
    font-display: swap;
    src: url('./assets/font/roboto-v19-latin-regular.eot');
    src:
      local('Roboto'),
      local('Roboto-Regular'),
      url('./assets/font/roboto-v19-latin-regular.woff2') format('woff2'),
      url('./assets/font/roboto-v19-latin-regular.woff') format('woff'),
      url('./assets/font/roboto-v19-latin-regular.ttf') format('truetype');
    unicode-range: U+000-5FF, U+20AC; /* Latin */
}

body {
  min-height: 100%;
}

#app {
  font-family: "Lato", "Helvetica", "Arial", "sans-serif";
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

.big-noodle {
  font-family: "Big Noodle", "Helvetica", "Arial", "sans-serif";
}

.oblique {
  font-style: oblique;
}

.text-jaffa {
  color: #f38d40;
}

.h-75px {
  height: 75px;
}

a {
  color: inherit;
}

a:hover {
  color: inherit;
  text-decoration: none;
}

.bgc-dark {
  background-color: #3c3c3e;
  color: #f8f9fa;
}

.bgc-deepdark {
  background-color: #2e2e2e;
  color: #f8f9fa;
}

.bgc-softdark {
  background-color: #4d4d4f;
  color: #f8f9fa;
}

.pointer:hover {
  cursor: pointer;
}

.border-jaffa {
  border-color: #f38d40;
}

.size-25 {
  font-size: 2.5rem;
}

.lh-15 {
  line-height: 1.5;
}

.top-0 {
  top: 0;
}
</style>
