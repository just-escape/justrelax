<template>
  <div id="app" class="h-100">
    <router-view/>
  </div>
</template>

<script>
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

.z-index-50 {
  z-index: 50;
}

.bg-black-transparent {
  background-color: rgba(0, 0, 0, 0.9);
}

.bg-black {
  background-color: #000000;
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

.blinking {
  animation: blinker 4s linear infinite;
}

@keyframes blinker {
  0% {
    opacity: 0;
  }
  25% {
    opacity: 0;
  }
  75% {
    opacity: 1;
  }
  100% {
    opacity: 0;
  }
}

.blinking-longer {
  animation: blinker-longer 6s linear infinite;
}

@keyframes blinker-longer {
  0% {
    opacity: 0;
  }
  25% {
    opacity: 0;
  }
  75% {
    opacity: 1;
  }
  100% {
    opacity: 0;
  }
}

.typed-element .typed-cursor {
  animation-duration: 1s
}
</style>
