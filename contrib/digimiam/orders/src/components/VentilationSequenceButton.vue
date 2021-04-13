<template>
    <span
      class="d-inline-block position-relative"
      @mousedown="mousedown"
      :style="{'opacity': display ? 1 : 0}"
      style="transition: opacity 2s ease-in-out;"
    >
      <div
        class="terminal-frame"
        :style="{
          background: 'rgb(' + buttonBgR + ', ' + buttonBgG + ', ' + buttonBgB + ')',
          color: 'rgb(' + buttonTextR + ', ' + buttonTextG + ', ' + buttonTextB + ')',
        }"
      >
        {{ $t('display_instructions') }}
      </div>
    </span>
</template>

<script>
export default {
  name: "VentilationSequenceButton",
  data() {
    return {
      buttonBgR: 0,
      buttonBgG: 0,
      buttonBgB: 0,
      buttonTextR: 253,
      buttonTextG: 246,
      buttonTextB: 227,
    }
  },
  methods: {
    mousedown: function() {
      this.$emit('mousedown')
      this.$anime.timeline({
        targets: this,
        easing: 'easeInOutQuad',
        duration: 200,
      })
      .add({
        buttonBgR: 253,
        buttonBgG: 246,
        buttonBgB: 227,
        buttonTextR: 0,
        buttonTextG: 0,
        buttonTextB: 0,
      })
      .add({
        buttonBgR: 0,
        buttonBgG: 0,
        buttonBgB: 0,
        buttonTextR: 253,
        buttonTextG: 246,
        buttonTextB: 227,
      })
    },
  },
  props: {
    display: Boolean,
  }
}
</script>

<style scoped>
.terminal-frame {
  background: none;
  color: var(--light);
  display: inline-block;
  padding: 10px 12px;
  position: relative;
  border: 3px var(--light) solid;
  box-shadow: -0.5em .5em transparentize(var(--light), 1);
  transform-origin: left bottom;
}

.terminal-frame:before, .terminal-frame:after {
  background: var(--light);
  border: 3px var(--light) solid;
  content: '';
  display: block;
  position: absolute;
}

.terminal-frame:before {
  left: -10px;
  top: 0px;
  height: 120%;
  transform: skewY(-45deg);
}

.terminal-frame:after {
  bottom: -10px;
  right: 0px;
  width: calc(100% + 7px);
  transform: skewX(-45deg);
}
</style>
