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
  },
}
</script>

<style>
@font-face {
  font-family: "Las Enter";
  font-style: normal;
  src: url('./assets/webfonts/LasEnter.ttf');
}

@font-face {
  font-family: "Name Smile";
  font-style: normal;
  src: url('./assets/webfonts/NameSmile.otf');
}

.text-las-enter {
  font-family: "Las Enter";
}

.text-name-smile {
  font-family: "Name Smile";
}

#app {
  font-family: 'Name Smile', 'sans-serif';
  position: relative;
  display: block;
  -webkit-user-select: none;
  -khtml-user-select: none;
  -moz-user-select: none;
  -ms-user-select: none;
  -o-user-select: none;
  user-select: none;
  color: var(--light);
  overflow: hidden;
}

#app::before {
  content: "";
  background: #03181f;
  position: absolute;
  right: 0;
  bottom: 0;
  left: 0;
  top: 0;
  z-index: -1;
}

.text-xxl {
  font-size: 100px;
  line-height: 1;
}

.text-xl {
  font-size: 70px;
  line-height: 1;
}

.text-l {
  font-size: 34px;
}

.text-teal {
  color: #00d1b6;
}

.text-orange {
  color: var(--orange);
}

.drop-shadow-teal {
  filter: drop-shadow(0 0 10px rgba(0, 209, 182, 0.4));
}

.drop-shadow-orange {
  filter: drop-shadow(0 0 10px rgba(253, 126, 20, 0.65));
}

.transition-transform {
  transition: transform 0.5s ease-in-out;
}

.pointer-events-none {
  pointer-events: none;
}

.pointer-events-auto {
  pointer-events: auto;
}
</style>