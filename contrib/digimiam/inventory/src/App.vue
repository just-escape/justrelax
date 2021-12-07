<template>
  <div id="app" class="h-100">
    <router-view/>
  </div>
</template>

<script>
import progressionStore from '@/store/progressionStore.js'
import publishSubscribeService from '@/store/publishSubscribeService.js'

export default {
  name: 'app',
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

    let blackScreen = this.$route.query.black_screen
    if (blackScreen && blackScreen === '0') {
      progressionStore.commit('displayBlackScreen', false)
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
  background: radial-gradient(ellipse at center, #03181f, rgb(3, 26, 34));
  position: relative;
  display: block;
  -webkit-user-select: none;
  -khtml-user-select: none;
  -moz-user-select: none;
  -ms-user-select: none;
  -o-user-select: none;
  user-select: none;
  color: var(--light);
}

.text-teal {
  color: #00d1b6;
}

.text-orange {
  color: orangered;
}

.glowing-container {
  border: 1px solid #00d1b6;
  box-shadow: 0px 0px 14px -6px rgba(0, 209, 182, 1);
}

.transition-1s {
  transition: all 1s;
}

.transition-400ms {
  transition: all 0.4s linear;
}

.transition-opacity-200ms {
  transition: opacity 0.2s;
}

.top-left {
  top: 0;
  left: 0;
}

.z-index-10 {
  z-index: 10;
}

.z-index-20 {
  z-index: 20;
}

.z-index-30 {
  z-index: 30;
}

.z-index-40 {
  z-index: 40;
}

.z-index-50 {
  z-index: 50;
}

.bg-black-transparent {
  background-color: rgba(0, 0, 0, 0.9);
}

.text-big {
  font-size: 300px;
}

.text-red {
  color: rgb(230, 0, 40);
}
</style>
