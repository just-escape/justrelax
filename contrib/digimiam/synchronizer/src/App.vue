<template>
  <div id="app" class="h-100">
    <router-view />
  </div>
</template>

<script>
import publishSubscribeService from '@/store/publishSubscribeService.js'
import lightStore from '@/store/lightStore.js'

export default {
  name: "app",
  methods: {
    ping() {
      setTimeout(this.ping, 5000)
      publishSubscribeService.commit('publish', {category: "ping"})
    }
  },
  computed: {
    isWebSocketOpened() {
      return publishSubscribeService.state.isWebSocketOpened
    },
  },
  watch: {
    isWebSocketOpened(newValue) {
      if (newValue) {
        let disabledColors = localStorage.getItem('disabledColors')
        if (disabledColors === null) {
          disabledColors = {"white": false, "orange": false, "blue": false, "green": false, "red": false, "pink": false}
        } else {
          disabledColors = JSON.parse(disabledColors)
        }
        for (let color in disabledColors) {
          lightStore.commit('setColorDisabled', {color: color, isDisabled: disabledColors[color]})
        }
      }
    },
  },
  mounted() {
    // Disable longtap (right click) menu to appear
    window.oncontextmenu = function() {
      return false;
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

    let ws_url = this.$route.query.ws_url;
    if (ws_url) {
      this.$connect("ws://" + ws_url);
    } else {
      this.$connect("ws://localhost:3031");
    }

    setTimeout(this.ping, 5000)
  }
};
</script>

<style>
@font-face {
  font-family: "Code New Roman";
  font-style: normal;
  src: url("./assets/webfonts/code-new-roman.woff2") format("woff2");
}

#app {
  font-family: "Code New Roman", "sans-serif";
  color: #ffffff;
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
  background: rgb(3, 26, 34);
  position: absolute;
  right: 0;
  bottom: 0;
  left: 0;
  top: 0;
  z-index: -1;
}

.w-large {
  width: 820px;
  padding: 0px 15px;
}

.w-small {
  width: 439.5px;
  padding: 0px 15px;
}

.text-teal {
  color: #00f6d1;
}

.text-orange {
  color: orangered;
}

video {
  display: block; /* Removes a mysterious margin bottom */
}

.glowing-container {
  border: 1px solid #00d1b6;
  box-shadow: 0px 0px 14px -6px rgba(0, 209, 182, 1);
}

.z-index-20 {
  z-index: 20;
}

.z-index-30 {
  z-index: 30;
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

.underline-dots {
  font-size: 18px;
  border-bottom: 1px dotted #ffffff;
  margin-bottom: 3px;
}

.pulse-opacity {
  animation: pulser 2s ease-in infinite;
}

@keyframes pulser {
	0% {
		opacity: 1;
	}
	60% {
		opacity: 0.3;
	}
	100% {
		opacity: 1;
	}
}
</style>
