<template>
  <div class="logs-container glowing-container h-100 p-3">
    <div class="logs-box d-flex flex-grow-1 w-100 position-relative mb-0 h-100">
      <div class="corner top-left"></div>
      <div class="corner top-right"></div>
      <div class="corner bottom-right"></div>

      <div class="logs w-100">
        <ul class="list-unstyled mb-0" id="scroll-bar">
          <li v-for="(log, index) in logs" :key="log.id" class="mb-2">
            <span v-if="log.level == 'warning'" class="warning">{{ $t('warning') }}&nbsp;</span>
            <span v-else-if="log.level == 'info'" class="info">{{ $t('info') }}&nbsp;</span>
            <span v-html="log.displayedMessage"></span>
            <span
              v-if="index == lastIndex"
              :style="{
                opacity: fullBlockOpacity,
              }"
            >&#9608;</span>
          </li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script>
import logStore from '@/store/logStore.js'

export default {
  name: 'Logs',
  data: function() {
    return {
      fullBlockOpacity: 1,
    }
  },
  computed: {
    lang: function() {
      return this.$i18n.locale
    },
    logs: function() {
      return logStore.state[this.lang].logs.filter(function(log) { return log.displayedChars >= 0 })
    },
    lastIndex: function() {
      return this.logs.length - 1
    },
  },
  methods: {
    scrollBottom: function() {
      var scrollBar = document.getElementById('scroll-bar')
      scrollBar.scrollTop = scrollBar.scrollHeight
    }
  },
  watch: {
    lang: function() {
      this.scrollBottom()
    },
    logs: function() {
      setTimeout(this.scrollBottom, 10)
    },
  },
  mounted: function() {
    this.$anime({
      targets: this,
      fullBlockOpacity: 0,
      duration: 500,
      loop: true,
      direction: 'alternate',
      easing: 'easeInOutExpo',
    })
  }
}
</script>

<style scoped>
.logs-container {
  border-top: 9px solid #00d1b6;
}

.logs-box {
  margin-bottom: 30px;
  padding: 5px;
  max-height: 396px;
}

.logs {
  padding-left: 8px;
  padding-top: 8px;
  padding-bottom: 8px;
  padding-right: 4px;
  font-family: "monospace";
}

.logs ul {
  font-size: 16px;
  line-height: 1;
  overflow-y: scroll;
  max-height: 100%;
  height: 100%;
}

.info {
  color: green;
}

.warning {
  color: orangered;
}

.logs ul::-webkit-scrollbar-track {
  box-shadow: inset 0 0 6px rgba(0, 0, 0, 0.9);
  background-color: transparent;
}

.logs ul::-webkit-scrollbar {
  width: 8px;
  background-color: transparent;
}

.logs ul::-webkit-scrollbar-thumb {
  box-shadow: inset 0 0 6px rgba(0, 0, 0, .5);
  background-color: #00d1b6;
}

.corner {
  position: absolute;
  height: 20px;
  width: 20px;
  filter: drop-shadow(0px 0px 1px rgba(0, 209, 182, 0.75));
}

.corner.top-left {
  top: 0;
  left: 0;
}

.corner.top-right {
  top: 0;
  right: 0;
}

.corner.bottom-right {
  bottom: 0;
  right: 0;
}

.corner::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  bottom: 0;
  right: 0;
  background-color: #00d1b6;
}

.corner.top-left::before {
  clip-path: polygon(
    0% 0%,
    100% 0%,
    100% 5px,
    5px 5px,
    5px 100%,
    0px 100%
  );
}

.corner.top-right::before {
  clip-path: polygon(
    0% 0%,
    100% 0%,
    100% 100%,
    calc(100% - 5px) 100%,
    calc(100% - 5px) 5px,
    5px 5px,
    0px 5px
  );
}

.corner.bottom-right::before {
  clip-path: polygon(
    calc(100% - 5px) 0%,
    100% 0%,
    100% 100%,
    0% 100%,
    0% calc(100% - 5px),
    calc(100% - 5px) calc(100% - 5px)
  );
}
</style>
