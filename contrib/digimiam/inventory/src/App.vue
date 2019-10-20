<template>
  <div
    id="app"
    @mousemove="mousemove"
    @mouseup="mouseup"
    @mouseleave="mouseleave"
    class="h-100 justify-content-center d-flex"
  >
    <Container/>
  </div>
</template>

<script>
import Container from '@/components/Container.vue'
import store from '@/store/store.js'

export default {
  name: 'app',
  components: {
    Container,
  },
  methods: {
    mousemove: function(event) {
      store.commit('appMousemove', event)
    },
    mouseup: function() {
      store.commit('appMouseup')
    },
    mouseleave: function() {
      store.commit('appMouseleave')
    },
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
  color: #00d1b6;
}
</style>
