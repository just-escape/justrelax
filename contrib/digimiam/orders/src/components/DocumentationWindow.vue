<template>
  <div
    class="documentation-window z-index-20 position-absolute"
    :style="{top: top, left: left, transform: transform}"
  >
    <Window :title="$t('terminal')" class="text-light text-code-new-roman" theme="primary">
      <div class="d-flex flex-column h-100 justify-content-center align-items-left bg-black">
        <div class="flex-grow-1 d-flex flex-row">
          <div class="position-relative w-100 mx-5 my-4">
            <div class="d-flex h-100 flex-column justify-content-between">
              <div>
                <div class="d-flex flex-column align-items-center mb-4">
                  <div v-for="(line, lineIndex) in tyrellVentimax" :key="lineIndex" v-html="getEscaped(line)"/>
                </div>
                <div class="terminal-frame w-100 mb-4">
                  >
                    <span class="position-absolute" style="left: 25px; overflow: hidden; width: calc(100% + 2px)">
                      <span id="typed-instruction"></span>
                      <vue-typed-js
                        :key="currentInstructionStringsKey"
                        :strings="currentInstructionStrings"
                        :class="currentInstructionClasses"
                        :cursorChar="'&#9608;'"
                        :loop="currentInstructionLoop"
                        :showCursor="currentInstructionStrings.length == 1 && currentInstructionStrings[0] != ''"
                      >
                        <div class="typing"></div>
                      </vue-typed-js>
                    </span>
                </div>
                <ul class="list-unstyled">
                  <li v-for="instruction in instructions" :key="instruction.locale">
                    <vue-typed-js
                      v-if="instruction.display"
                      :strings="[$t(instruction.locale)]"
                      @onComplete="onInstructionTypedComplete(instruction.locale)"
                      :class="instruction.classes"
                      :cursorChar="'&#9608;'"
                    >
                      <div :ref="'instruction-' + instruction.locale" class="typing"></div>
                    </vue-typed-js>
                  </li>
                </ul>
              </div>
              <VentilationSequenceButton
                class="mb-4"
                :style="{'margin-left': ventilationButtonOffset ? '3.5rem' : '0px'}"
                :display="displayVentilationSequenceButton"
                @mousedown="restartRound"
              />
            </div>
          </div>
        </div>
      </div>
    </Window>
  </div>
</template>

<script>
import Window from '@/components/Window.vue'
import VentilationSequenceButton from '@/components/VentilationSequenceButton.vue'
import progressionStore from '@/store/progressionStore.js'
import publishSubscribeService from '@/store/publishSubscribeService.js'

const PROGRESSION_START = 0
const PROGRESSION_ROUND_1 = 1
const PROGRESSION_ROUND_2 = 2
const PROGRESSION_ROUND_3 = 3

export default {
  name: "DocumentationWindow",
  components: {
    Window,
    VentilationSequenceButton,
  },
  data() {
    return {
      topOffset: 180,
      leftOffset: 420,
      scaleX: 0,
      scaleY: 0,
      tyrellVentimax: [
        // http://patorjk.com/software/taag/#p=display&f=Ivrit&t=Manuel%20technique
        '  _____               _ _  __     __         _   _                      ',
        ' |_   _|   _ _ __ ___| | | \\ \\   / /__ _ __ | |_(_)_ __ ___   __ ___  __',
        '   | || | | | \'__/ _ \\ | |  \\ \\ / / _ \\ \'_ \\| __| | \'_ ` _ \\ / _` \\ \\/ /',
        '   | || |_| | | |  __/ | |   \\ V /  __/ | | | |_| | | | | | | (_| |>  < ',
        '   |_| \\__, |_|  \\___|_|_|    \\_/ \\___|_| |_|\\__|_|_| |_| |_|\\__,_/_/\\_\\',
        '       |___/                                                            ',
      ],
      displayVentilationSequenceButton: false,
      progression: PROGRESSION_START,
      typing: false,
      instructionsDisplayQueue: [],
      instructions: [
        {
          locale: 'air_ducts',
          display: false,
          displayAtProgression: PROGRESSION_ROUND_1,
          classes: ['mb-3'],
        },
        {
          locale: 'refectory',
          display: false,
          displayAtProgression: PROGRESSION_ROUND_1,
          classes: ['ml-3'],
        },
        {
          locale: 'pantry',
          display: false,
          displayAtProgression: PROGRESSION_ROUND_1,
          classes: ['ml-3'],
        },
        {
          locale: 'server_room',
          display: false,
          displayAtProgression: PROGRESSION_ROUND_1,
          classes: ['ml-3', 'mb-4'],
        },
        {
          locale: 'air_sources',
          display: false,
          displayAtProgression: PROGRESSION_ROUND_1,
          classes: ['mb-3'],
        },
        {
          locale: 'purified_air',
          display: false,
          displayAtProgression: PROGRESSION_ROUND_1,
          classes: ['ml-3'],
        },
        {
          locale: 'half_purified_air',
          display: false,
          displayAtProgression: PROGRESSION_ROUND_1,
          classes: ['position-relative ml-3'],
        },
        {
          locale: 'polluted_air',
          display: false,
          displayAtProgression: PROGRESSION_ROUND_1,
          classes: ['ml-3 mb-4'],
        },
        {
          locale: 'sequence_code',
          display: false,
          displayAtProgression: PROGRESSION_ROUND_1,
          classes: ['mb-3'],
        },
        {
          locale: 'sequence_white',
          display: false,
          displayAtProgression: PROGRESSION_ROUND_1,
          classes: ['ml-3'],
        },
        {
          locale: 'sequence_yellow',
          display: false,
          displayAtProgression: PROGRESSION_ROUND_1,
          classes: ['ml-3'],
        },
        {
          locale: 'sequence_orange',
          display: false,
          displayAtProgression: PROGRESSION_ROUND_2,
          classes: ['ml-3'],
        },
        {
          locale: 'sequence_blue',
          display: false,
          displayAtProgression: PROGRESSION_ROUND_2,
          classes: ['ml-3'],
        },
        {
          locale: 'sequence_pink',
          display: false,
          displayAtProgression: PROGRESSION_ROUND_2,
          classes: ['ml-3'],
        },
        {
          locale: 'sequence_purple',
          display: false,
          displayAtProgression: PROGRESSION_ROUND_3,
          classes: ['ml-3'],
        },
      ],
    }
  },
  computed: {
    ventilationButtonOffset() {
      return this.$route.query.ventilation_button_offset && this.$route.query.ventilation_button_offset != '0'
    },
    top() {
      return "calc(0px + " + this.topOffset + "px)"
    },
    left() {
      return "calc(0px + " + this.leftOffset + "px)"
    },
    transform() {
      return "scaleX(" + this.scaleX + ") scaleY(" + this.scaleY + ")"
    },
    displayed() {
      return progressionStore.state.showDocumentation
    },
    currentInstructionStrings() {
      if (progressionStore.state.currentInstructionStringsUseLocale) {
        return progressionStore.state.currentInstructionStrings.map(s => this.$t(s))
      } else {
        return progressionStore.state.currentInstructionStrings
      }
    },
    currentInstructionStringsKey() {
      // If this value changes, the instruction is deleted and typed again (because the content or locale changed)
      if (progressionStore.state.currentInstructionStringsUseLocale) {
        return this.locale + JSON.stringify(this.currentInstructionStrings) + Math.random()
      } else {
        return JSON.stringify(this.currentInstructionStrings) + Math.random()
      }
    },
    currentInstructionClasses() {
      return []
    },
    currentInstructionLoop() {
      return progressionStore.state.currentInstructionLoop
    },
    getEscaped() {
      return function(string) {
        return string.replace(/ /g, "&nbsp;")
      }
    },
    puzzleRound() {
      return progressionStore.state.round
    },
    locale() {
      return this.$i18n.locale
    },
  },
  methods: {
    restartRound() {
      publishSubscribeService.commit('publish', {'category': 'restart_round'})
    },
    nextInstruction() {
      this.typing = true
      if (this.instructionsDisplayQueue.length > 0) {
        let nextInstructionIndex = this.instructionsDisplayQueue.shift()
        this.instructions[nextInstructionIndex].display = true
      } else {
        this.typing = false
        // Special case, when all PROGRESSION_ROUND_1 instructions have been typed
        if (this.progression == PROGRESSION_ROUND_1) {
          this.displayVentilationSequenceButton = true
        }
      }
    },
    onInstructionTypedComplete(locale) {
      this.$refs['instruction-' + locale][0].nextSibling.style.display = 'none'
      this.nextInstruction()
    },
    computeCurrentProgressionInstructionsToDisplay() {
      for (let [index, instruction] of Object.values(this.instructions).entries()) {
        if (this.progression >= instruction.displayAtProgression && instruction.display === false && !this.instructionsDisplayQueue.includes(index)) {
          this.instructionsDisplayQueue.push(index)
        }
      }
    }
  },
  mounted() {
    // Those lines are not supposed to do anything but are just in case one day some instruction
    // needs to be displayed while still being at PROGRESSION_START
    this.computeCurrentProgressionInstructionsToDisplay()
    this.nextInstruction()
  },
  watch: {
    displayed(newValue) {
      if (newValue) {
        this.$anime({
          targets: this,
          scaleX: 1,
          scaleY: 1,
          duration: 400,
          easing: 'easeInQuad',
        })
      } else {
        this.$anime({
          targets: this,
          scaleX: 0,
          scaleY: 0,
          duration: 700,
          easing: 'easeInOutQuad',
        })
      }
    },
    puzzleRound(newValue) {
      if (newValue === 1) {
        this.progression = PROGRESSION_ROUND_1
      } else if (newValue === 2) {
        this.progression = PROGRESSION_ROUND_2
      } else if (newValue === 3) {
        this.progression = PROGRESSION_ROUND_3
      }
    },
    progression() {
      this.computeCurrentProgressionInstructionsToDisplay()
      if (!this.typing) {
        this.nextInstruction()
      }
    },
    locale() {
      for (let instruction of this.instructions) {
        instruction.display = false
      }
      this.instructionsDisplayQueue = []
      this.computeCurrentProgressionInstructionsToDisplay()
      setTimeout(this.nextInstruction, 100)
    },
  }
}
</script>

<style>
.duct {
  color: #00b1d6;
  font-weight: bold;
}

.source {
  color: #007bff;
  font-weight: bold;
}

.half-left {
  clip-path: polygon(
    0% -20%,
    47% -20%,
    47% 120%,
    0% 120%
  );
}

.half-right {
  clip-path: polygon(
    53% -20%,
    100% -20%,
    100% 120%,
    53% 120%
  );
}

.text-yellow {
  color: var(--yellow);
}

.text-orange {
  color: var(--orange);
}
</style>

<style scoped>
.documentation-window {
  width: 1080px;
  height: 720px;
  color: rgb(253, 246, 227);
  font-family: "Monospace";
  line-height: 1;
}

.button-reduce {
  border: 1px solid rgb(15, 30, 35);
  border-radius: 2px;
  line-height: 1;
  padding: 2px 2px 0px 2px;
}

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