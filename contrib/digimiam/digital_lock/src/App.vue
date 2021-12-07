<template>
  <div id="app" class="h-100">
    <router-view/>
  </div>
</template>

<script>
import publishSubscribeService from '@/store/publishSubscribeService.js'

export default {
  name: 'App',
  methods: {
    ping() {
      setTimeout(this.ping, 5000)
      publishSubscribeService.commit('publish', {category: "ping"})
    }
  },
  mounted() {
    // Disable longtap (right click) menu to appear
    window.oncontextmenu = function() {
      return false
    }

    if (this.$route.query.channel_prefix !== undefined) {
      publishSubscribeService.commit('addSubscriptionChannel', this.$route.query.channel_prefix + '.' + publishSubscribeService.state.name)
      publishSubscribeService.commit('addSubscriptionChannel', this.$route.query.channel_prefix + '.broadcast')
      publishSubscribeService.commit('setPublicationChannel', this.$route.query.channel_prefix + '.scenario')
    } else {
      publishSubscribeService.commit('addSubscriptionChannel', publishSubscribeService.state.name)
      publishSubscribeService.commit('addSubscriptionChannel', 'broadcast')
      publishSubscribeService.commit('setPublicationChannel', 'scenario')
    }

    let ws_url = this.$route.query.ws_url
    if (ws_url) {
      this.$connect('ws://' + ws_url)
    } else {
      this.$connect('ws://localhost:3031')
    }

    setTimeout(this.ping, 5000)
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
  background: radial-gradient(ellipse at center, #03181f, rgb(3, 26, 34));
  position: absolute;
  right: 0;
  bottom: 0;
  left: 0;
  top: 0;
  z-index: -1;
}
</style>
