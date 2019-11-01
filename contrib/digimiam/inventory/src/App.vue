<template>
  <div
    id="app"
    @mousemove="mousemove"
    @mouseup="mouseup"
    @mouseleave="mouseleave"
    class="h-100 justify-content-center d-flex position-relative"
  >
    <BackgroundLines/>
    <div class="padding-top-10px">
      <Container/>
    </div>
  </div>
</template>

<script>
import BackgroundLines from '@/components/BackgroundLines.vue'
import Container from '@/components/Container.vue'
import store from '@/store/store.js'

export default {
  name: 'app',
  components: {
    BackgroundLines,
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
  background: radial-gradient(ellipse at center, #03181f, rgb(3, 26, 34));
  position: relative;
  display: block;
  -webkit-user-select: none;
  -khtml-user-select: none;
  -moz-user-select: none;
  -ms-user-select: none;
  -o-user-select: none;
  user-select: none;
}

.padding-top-10px {
  padding-top: 10px;
}

.text-teal {
  color: #00d1b6;
}
</style>
