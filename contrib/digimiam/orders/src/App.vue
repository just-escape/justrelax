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

@font-face {
    font-family: "Gotham";
    font-style: normal;
    src: url('./assets/webfonts/gotham-book.otf') format('otf');
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

.glowing-container {
  /*border: 1px solid #00d1b6;*/
  border: 1px solid black;
  /*box-shadow: 0px 0px 14px -6px rgba(0, 209, 182, 1);*/
  box-shadow: 0px 0px 14px -6px black;
}

.lh-1 {
  line-height: 1;
}

.lh-13 {
  line-height: 1.3;
}

.underline-dots {
  border-bottom: 1px dotted black;
  margin-bottom: 3px;
}

.underline-dots-white {
  border-bottom: 1px dotted white;
  margin-bottom: 3px;
}

.text-white {
  color: white;
}

.shadow-box-dark {
  box-shadow: 1px 1px 5px var(--dark);
}

.size-12 {
  font-size: 1.2rem;
}
</style>
