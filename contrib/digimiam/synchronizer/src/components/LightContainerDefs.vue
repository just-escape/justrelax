<template>
  <defs>
    <linearGradient id="activation-left-right" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop
        class="gradientColor1"
        offset="0%"
        :stop-color="colorValidated"
      />
      <stop
        class="gradientColor2"
        offset="10%"
        :stop-color="colorActivation"
      />
    </linearGradient>
    <linearGradient id="activation-right-left" x1="100%" y1="0%" x2="0%" y2="0%">
      <stop
        class="gradientColor1"
        offset="0%"
        :stop-color="colorValidated"
      />
      <stop
        class="gradientColor2"
        offset="10%"
        :stop-color="colorActivation"
      />
    </linearGradient>
    <linearGradient id="activation-topleft-bottomright" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop
        class="gradientColor1"
        offset="0%"
        :stop-color="colorValidated"
      />
      <stop
        class="gradientColor2"
        offset="10%"
        :stop-color="colorActivation"
      />
    </linearGradient>
    <linearGradient id="activation-topright-bottomleft" x1="100%" y1="0%" x2="0%" y2="100%">
      <stop
        class="gradientColor1"
        offset="0%"
        :stop-color="colorValidated"
      />
      <stop
        class="gradientColor2"
        offset="10%"
        :stop-color="colorActivation"
      />
    </linearGradient>
    <linearGradient id="activation-bottomleft-topright" x1="0%" y1="100%" x2="100%" y2="0%">
      <stop
        class="gradientColor1"
        offset="0%"
        :stop-color="colorValidated"
      />
      <stop
        class="gradientColor2"
        offset="10%"
        :stop-color="colorActivation"
      />
    </linearGradient>
    <linearGradient id="activation-bottomright-topleft" x1="100%" y1="100%" x2="0%" y2="0%">
      <stop
        class="gradientColor1"
        offset="0%"
        :stop-color="colorValidated"
      />
      <stop
        class="gradientColor2"
        offset="10%"
        :stop-color="colorActivation"
      />
    </linearGradient>

    <linearGradient id="final-animation-left-right" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop
        class="gradientColor1"
        offset="0%"
        :stop-color="colorValidated"
      />
      <stop
        class="gradientColor2"
        offset="10%"
        :stop-color="colorDefault"
      />
    </linearGradient>
    <linearGradient id="final-animation-right-left" x1="100%" y1="0%" x2="0%" y2="0%">
      <stop
        class="gradientColor1"
        offset="0%"
        :stop-color="colorValidated"
      />
      <stop
        class="gradientColor2"
        offset="10%"
        :stop-color="colorDefault"
      />
    </linearGradient>
    <linearGradient id="final-animation-topleft-bottomright" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop
        class="gradientColor1"
        offset="0%"
        :stop-color="colorValidated"
      />
      <stop
        class="gradientColor2"
        offset="10%"
        :stop-color="colorDefault"
      />
    </linearGradient>
    <linearGradient id="final-animation-topright-bottomleft" x1="100%" y1="0%" x2="0%" y2="100%">
      <stop
        class="gradientColor1"
        offset="0%"
        :stop-color="colorValidated"
      />
      <stop
        class="gradientColor2"
        offset="10%"
        :stop-color="colorDefault"
      />
    </linearGradient>
    <linearGradient id="final-animation-bottomleft-topright" x1="0%" y1="100%" x2="100%" y2="0%">
      <stop
        class="gradientColor1"
        offset="0%"
        :stop-color="colorValidated"
      />
      <stop
        class="gradientColor2"
        offset="10%"
        :stop-color="colorDefault"
      />
    </linearGradient>
    <linearGradient id="final-animation-bottomright-topleft" x1="100%" y1="100%" x2="0%" y2="0%">
      <stop
        class="gradientColor1"
        offset="0%"
        :stop-color="colorValidated"
      />
      <stop
        class="gradientColor2"
        offset="10%"
        :stop-color="colorDefault"
      />
    </linearGradient>

    <linearGradient id="activation-path-animation-left-right" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop
        class="gradientColor1"
        offset="0%"
        :stop-color="colorActivation"
      />
      <stop
        class="gradientColor2"
        offset="10%"
        :stop-color="colorDefault"
      />
    </linearGradient>
    <linearGradient id="activation-path-animation-right-left" x1="100%" y1="0%" x2="0%" y2="0%">
      <stop
        class="gradientColor1"
        offset="0%"
        :stop-color="colorActivation"
      />
      <stop
        class="gradientColor2"
        offset="10%"
        :stop-color="colorDefault"
      />
    </linearGradient>
    <linearGradient id="activation-path-animation-topleft-bottomright" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop
        class="gradientColor1"
        offset="0%"
        :stop-color="colorActivation"
      />
      <stop
        class="gradientColor2"
        offset="10%"
        :stop-color="colorDefault"
      />
    </linearGradient>
    <linearGradient id="activation-path-animation-topright-bottomleft" x1="100%" y1="0%" x2="0%" y2="100%">
      <stop
        class="gradientColor1"
        offset="0%"
        :stop-color="colorActivation"
      />
      <stop
        class="gradientColor2"
        offset="10%"
        :stop-color="colorDefault"
      />
    </linearGradient>
    <linearGradient id="activation-path-animation-bottomleft-topright" x1="0%" y1="100%" x2="100%" y2="0%">
      <stop
        class="gradientColor1"
        offset="0%"
        :stop-color="colorActivation"
      />
      <stop
        class="gradientColor2"
        offset="10%"
        :stop-color="colorDefault"
      />
    </linearGradient>
    <linearGradient id="activation-path-animation-bottomright-topleft" x1="100%" y1="100%" x2="0%" y2="0%">
      <stop
        class="gradientColor1"
        offset="0%"
        :stop-color="colorActivation"
      />
      <stop
        class="gradientColor2"
        offset="10%"
        :stop-color="colorDefault"
      />
    </linearGradient>

    <filter id="glowing" x="-50" y="-50" width="150" height="150">
      <feGaussianBlur result="blurOut" in="offOut" stdDeviation="1.7" />
      <feBlend in="SourceGraphic" in2="blurOut" mode="normal" />
    </filter>
    <filter id="glowing-transition" x="-50" y="-50" width="150" height="150">
      <feGaussianBlur id="glowing-transition-intensity" result="blurOut" in="offOut" stdDeviation="2" />
      <feBlend in="SourceGraphic" in2="blurOut" mode="normal" />
    </filter>
    <filter id="glowing-more" x="-50" y="-50" width="150" height="150">
      <feGaussianBlur result="blurOut" in="offOut" stdDeviation="20" />
      <feBlend in="SourceGraphic" in2="blurOut" mode="normal" />
    </filter>
  </defs>
</template>

<script>
import lightStore from '@/store/lightStore.js'

export default {
  name: 'LightContainerGradients',
  computed: {
    colorDefault: function() {
      return lightStore.state.colorDefault
    },
    colorActivation: function() {
      return lightStore.state.colorActivation
    },
    colorValidated: function() {
      return lightStore.state.colorValidated
    },
  }
}
</script>