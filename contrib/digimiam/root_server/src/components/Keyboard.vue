<template>
  <div class="position-relative w-100 h-100 p-3">
    <div
      class="position-absolute keyboard-offset transition-1s"
      :class="{'grayscale': !isKeyboardActive}"
      :style="{opacity: opacity}"
    >
      <KeyboardSpaceBar
        :top="149.5" :left="317"
        :width="227.5" :height="105"
        :character="' '"
      />
      <KeyboardLetter
        v-for="(letter, letterIndex) in layout" :key="'letter-' + letterIndex"
        :top="letter.top" :left="letter.left" :width="70"
        :character="letter.character"
      />
      <KeyboardDodecagon
        v-for="(special, specialIndex) in specialActions" :key="'special-' + specialIndex"
        :top="special.top" :left="special.left" :width="122.5" :height="140"
        :mirror="special.mirror"
        :character="special.character"
      />
    </div>
  </div>
</template>

<script>
import KeyboardDodecagon from '@/components/KeyboardDodecagon.vue'
import KeyboardSpaceBar from '@/components/KeyboardSpaceBar.vue'
import KeyboardLetter from '@/components/KeyboardLetter.vue'
import keyboardStore from '@/store/keyboardStore.js'

export default {
  name: "Keyboard",
  components: {
    KeyboardDodecagon,
    KeyboardSpaceBar,
    KeyboardLetter,
  },
  data() {
    return {
      opacity: 0,
      specialActions: [
        {
          top: -4,
          left: 741,
          character: 'BACKSPACE',
          mirror: true,
        },
        {
          top: 120,
          left: 739,
          character: 'CR',
          mirror: false,
        },
      ],
      layout: [
        {
          top: 27.5,
          left: 157.5,
          character: 'a',
        },
        {
          top: 27.5,
          left: 264,
          character: 'c',
        },
        {
          top: -3,
          left: 317,
          character: 'd',
        },
        {
          top: 27.5,
          left: 370,
          character: 'e',
        },
        {
          top: -3,
          left: 423,
          character: 'f',
        },
        {
          top: 27.5,
          left: 476,
          character: 'g',
        },
        {
          top: -3,
          left: 529,
          character: 'h',
        },
        {
          top: 27.5,
          left: 582,
          character: 'i',
        },
        {
          top: -3,
          left: 635,
          character: 'j',
        },
        {
          top: 88.5,
          left: 157.5,
          character: 'k',
        },
        {
          top: 58,
          left: 211,
          character: 'b',
        },
        {
          top: 88.5,
          left: 264,
          character: 'm',
        },
        {
          top: 58,
          left: 317,
          character: 'n',
        },
        {
          top: 88.5,
          left: 370,
          character: 'o',
        },
        {
          top: 58,
          left: 423,
          character: 'p',
        },
        {
          top: 88.5,
          left: 476,
          character: 'q',
        },
        {
          top: 58,
          left: 529,
          character: 'r',
        },
        {
          top: 88.5,
          left: 582,
          character: 's',
        },
        {
          top: 58,
          left: 635,
          character: 't',
        },
        {
          top: 149.5,
          left: 157.5,
          character: 'u',
        },
        {
          top: 119,
          left: 211,
          character: 'l',
        },
        {
          top: 149.5,
          left: 264,
          character: 'w',
        },
        {
          top: 119,
          left: 317,
          character: 'x',
        },
        {
          top: 119,
          left: 423,
          character: 'y',
        },
        {
          top: 119,
          left: 529,
          character: 'z',
        },
        {
          top: 119,
          left: 635,
          character: '\'',
        },
        {
          top: 180,
          left: 211,
          character: 'v',
        },
      ],
    }
  },
  computed: {
    isKeyboardActive() {
      return keyboardStore.state.displayPasswordWindow || keyboardStore.state.displayPasswordRecoveryWindow
    },
  },
  watch: {
    isKeyboardActive(newValue) {
      if (newValue) {
        this.$anime({
          targets: this,
          opacity: 1,
          duration: 5000,
          easing: 'linear',
        })
      }
    },
  },
}
</script>

<style scoped>
.keyboard-offset {
  left: -80px;
  top: 0px;
}

.grayscale {
  filter: grayscale(70%);
}
</style>