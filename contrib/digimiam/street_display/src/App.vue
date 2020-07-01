<template>
  <div id="app" class="h-100">
    <router-view/>
  </div>
</template>

<script>
export default {
  name: 'App',
  mounted() {
    let ws_url = this.$route.query.ws_url
    if (ws_url) {
      this.$connect('ws://' + ws_url)
    } else {
      this.$connect('ws://localhost:3031')
    }
  },
}
</script>
