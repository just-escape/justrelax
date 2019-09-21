<template>
  <div class="d-flex flex-grow-1 flex-column">
    <div class="logs-box d-flex flex-grow-1 w-100 position-relative mb-1">
      <div class="logs-top-left-corner"></div>
      <div class="logs-top-right-corner"></div>
      <div class="logs-bottom-right-corner"></div>
      <div class="logs w-100">
        <ul class="list-unstyled mb-0" id="scroll-bar">
          <li v-for="(log, index) in logs" :key="log.id" class="mb-2">
            <span v-if="log.level == 'warning'" class="warning">Warning: </span>
            <span v-else-if="log.level == 'info'" class="info">Info: </span>
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
import store from '@/store/store.js'

export default {
  name: 'Logs',
  data: function() {
    return {
      fullBlockOpacity: 1,
    }
  },
  computed: {
    carriageReturns: function() {
      return store.state.carriageReturns
    },
    logs: function() {
      return store.state.logs.filter(function(log) { return log.displayedChars >= 0})
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
    carriageReturns: function() {
      setTimeout(this.scrollBottom, 10)
    }
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
.title {
  font-size: 14px;
}

.logs-box {
  margin-bottom: 30px;
  padding: 5px;
}

.logs {
  padding-left: 8px;
  padding-top: 8px;
  padding-bottom: 8px;
  padding-right: 4px;
  max-height: 800px;
}

.logs ul {
  font-size: 14px;
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

.logs-top-left-corner {
  position: absolute;
  top: 0;
  left: 0;
  height: 20px;
  width: 20px;
  border-left: 5px solid #00d1b6;
  border-top: 5px solid #00d1b6;
}

.logs-top-right-corner {
  position: absolute;
  top: 0;
  right: 0;
  height: 20px;
  width: 20px;
  border-right: 5px solid #00d1b6;
  border-top: 5px solid #00d1b6;
}

.logs-bottom-left-corner {
  position: absolute;
  bottom: 0;
  left: 0;
  height: 20px;
  width: 20px;
  border-left: 5px solid #00d1b6;
  border-bottom: 5px solid #00d1b6;
}

.logs-bottom-right-corner {
  position: absolute;
  bottom: 0;
  right: 0;
  height: 20px;
  width: 20px;
  border-right: 5px solid #00d1b6;
  border-bottom: 5px solid #00d1b6;
}
</style>
