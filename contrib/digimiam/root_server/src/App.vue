<template>
  <div id="app" class="d-flex justify-content-center position-relative h-100">
    <Background/>
    <PasswordWindow/>
  </div>
</template>

<script>
import Background from './components/Background.vue'
import PasswordWindow from './components/PasswordWindow.vue'

export default {
  name: 'app',
  components: {
    Background,
    PasswordWindow,
  },
  mounted() {
    this.$connect()
  },
}
</script>

<style>
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
