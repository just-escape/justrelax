<template>
  <g>
    <polygon
      points="87,80 93,80 93,-10 87,-10"
      fill="#00f1d6"
      filter="url(#glowing-more)"
    />
    <circle
      cx="90"
      cy="80"
      r="40"
      fill="#00f1d6"
      filter="url(#glowing-more)"
    />
    <path
      :d="get"
      stroke="#00f1d6"
      stroke-width="6"
      filter="url(#glowing-more)"
    />
    <circle
      cx="150"
      cy="110"
      r="20"
      fill="#00f1d6"
      filter="url(#glowing-more)"
    />
  </g>
</template>

<script>
import lightStore from '@/store/lightStore.js'

export default {
  name: 'LightContainerGenerator.vue',
  computed: {
    get: function() {
      var x = lightStore.state.generatorWireX
      var y = lightStore.state.generatorWireY
      return 'M150 110 L ' + x + ' ' + y
    }
  }
}
</script>