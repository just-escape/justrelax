<template>
  <div class="documentation d-flex flex-column" :style="{top: terminalTop}">
    <div class="flex-grow-1 d-flex flex-row">
      <div class="position-relative w-50 border-white border-right-thick">
        <div v-for="(line, lineIndex) in asciiPanel" :key="'line-' + lineIndex" v-html="getEscaped(line)"/>
        <i
          v-for="(icon, iconIndex) in panelIcons" :key="'icon-' + iconIndex"
          class="position-absolute"
          :class="icon.classes"
          :style="{top: icon.top, left: icon.left}"
        />
      </div>
      <div class="position-relative w-50 border-white border-left-thick">
        <div class="d-flex flex-column align-items-center mb-3">
          <div v-for="(line, lineIndex) in tyrellVentimax" :key="lineIndex" v-html="getEscaped(line)"/>
        </div>
        <div class="pl-2">
          <div :style="{color: unplugBeforeInterventionColor}" class="mb-4">{{ $t('unplug_before_intervention') }}</div>
          <div class="mb-3">{{ $t('air_ducts') }}</div>
          <ul class="list-unstyled ml-3 mb-4">
            <li><i class="text-primary fas fa-utensils fa-fw"/> {{ $t('refectory') }}</li>
            <li><i class="text-green fa fa-cubes fa-fw"/> {{ $t('pantry') }}</li>
            <li><i class="text-teal fa fa-server fa-fw"/> {{ $t('server_room') }}</li>
          </ul>
          <div class="mb-3">{{ $t('air_sources') }}</div>
          <ul class="list-unstyled ml-3 mb-4">
            <li><i class="fa fa-recycle fa-fw"/> {{ $t('purified_air') }}</li>
            <li class="position-relative">
              <i class="text-yellow position-absolute fa fa-recycle fa-fw half-left"/><i class="text-yellow fa fa-biohazard fa-fw half-right"/>
              {{ $t('half_purified_air') }}
            </li>
            <li><i class="text-orange fa fa-biohazard fa-fw"/> {{ $t('polluted_air') }}</li>
          </ul>
          <div class="mb-3">{{ $t('sequence_code') }}</div>
          <ul class="list-unstyled ml-3 mb-4">
            <li v-for="(i, iIndex) in displayedInstructions" :key="iIndex">
              {{ i.instruction.slice(0, i.displayedChars) }}<span v-if="i.typing" :style="{opacity: underscoreOpacity}">_</span>
            </li>
          </ul>
        </div>
        <div class="position-absolute bottom-right">{{ $t('documentation_generated') }}</div>
      </div>
    </div>
    <div class="menu-line flex-shrink-1">
      <div class="mt-1 mx-1">
        {{ $t('terminal_label') }}
      </div>
    </div>
  </div>
</template>

<script>
import progressionStore from '@/store/progressionStore.js'

export default {
  name: "VentilatorsDocumentation",
  data() {
    return {
      underscoreOpacity: 0,
      asciiPanel: [
        ' ',
        '                          ______________________________________',
        '                          \\____________________________________/',
        ' ',
        '                      |\\                                          /|',
        '                      | |                                        | |',
        '                      | |   +----------+                         | |',
        '                      | |   |  @@  @@  |                         | |',
        '                      | |   | @@    @@ |                         | |',
        '                      | |   | @      @ |                 ( )     | |',
        '                      | |   |    @@    |  ( )                    | |',
        '                      | |   |   @@@@   |   \\\\          ( ) ( )   | |',
        '                      | |   +----------+    \\\\                   | |',
        '                      | |                    -\\\\                 | |',
        '                      |/                       -\\\\                \\|',
        '                                                 +->  ',
        '                        /|                                      |\\',
        '                       | |                                      | |',
        '                       | |  +----------+                        | |',
        '                       | |  |  @@  @@  |                        | |',
        '                       | |  | @@    @@ |                        | |',
        '                       | |  | @      @ |                 ( )    | |',
        '                       | |  |    @@    |  ( )                   | |',
        '                       | |  |   @@@@   |   \\\\          ( ) ( )  | |',
        '                       | |  +----------+    \\\\                  | |',
        '                       | |                   -\\\\                | |',
        '                        \\|                     \\\\               |/ ',
        '                                                \\\\                ',
        '                      |\\                         +->              /|',
        '                      | |                                        | |',
        '                      | |   +----------+                         | |',
        '                      | |   |  @@  @@  |                         | |',
        '                      | |   | @@    @@ |                         | |',
        '                      | |   | @      @ |                 ( )     | |',
        '                      | |   |    @@    |  ( )                    | |',
        '                      | |   |   @@@@   |   \\\\          ( ) ( )   | |',
        '                      | |   +----------+    -\\\\                  | |',
        '                      | |                     -\\\\                | |',
        '                      |/                        +->               \\|',
        '                           ___________               ___________',
        '                          /___________| [ ] [ ] [ ] |___________\\ ',
        ' ',
        ' ',
        ' ',
        ' ',
      ],
      panelIcons: [
        {
          classes: "text-primary fas fa-utensils fa-fw fa-lg",
          top: "126px",
          left: "405px",
        },
        {
          classes: "text-green fa fa-cubes fa-fw fa-lg",
          top: "319px",
          left: "405px",
        },
        {
          classes: "text-teal fa fa-server fa-fw fa-lg",
          top: "512px",
          left: "405px",
        },
        {
          classes: "fa fa-recycle fa-fw fa-lg",
          top: "112px",
          left: "550px",
        },
        {
          classes: "text-yellow fa fa-recycle fa-fw half-left fa-lg",
          top: "305px",
          left: "550px",
        },
        {
          classes: "text-yellow fa fa-biohazard fa-fw half-right fa-lg",
          top: "305px",
          left: "550px",
        },
        {
          classes: "text-orange fa fa-biohazard fa-fw fa-lg",
          top: "498px",
          left: "550px",
        },
      ],
      tyrellVentimax: [
        // http://patorjk.com/software/taag/#p=display&f=Ivrit&t=Manuel%20technique
        '  _____               _ _  __     __         _   _                      ',
        ' |_   _|   _ _ __ ___| | | \\ \\   / /__ _ __ | |_(_)_ __ ___   __ ___  __',
        '   | || | | | \'__/ _ \\ | |  \\ \\ / / _ \\ \'_ \\| __| | \'_ ` _ \\ / _` \\ \\/ /',
        '   | || |_| | | |  __/ | |   \\ V /  __/ | | | |_| | | | | | | (_| |>  < ',
        '   |_| \\__, |_|  \\___|_|_|    \\_/ \\___|_| |_|\\__|_|_| |_| |_|\\__,_/_/\\_\\',
        '       |___/                                                            ',
      ],
      typing: {
        fr: {
          queue: [],
          task: null,
        },
        en: {
          queue: [],
          task: null,
        },
      },
      colorInstructions: {
        fr: [
          {
            displayedChars: 100,
            instruction: '* blanc : brancher le conduit à la source d\'air purifié',
            typing: false,
          },
          {
            displayedChars: 100,
            instruction: '* jaune : brancher le conduit à la source d\'air semi-purifié',
            typing: false,
          },
          {
            displayedChars: 0,
            instruction: '* orange : brancher le conduit à la source d\'air pollué',
            typing: false,
          },
          {
            displayedChars: 0,
            instruction: '* bleu : brancher le conduit à une source d\'air plus pur',
            typing: false,
          },
          {
            displayedChars: 0,
            instruction: '* rose : appliquer à ce conduit le code séquence du conduit précédent',
            typing: false,
          },
          {
            displayedChars: 0,
            instruction: '* violet : appliquer à ce conduit le code séquence du conduit suivant',
            typing: false,
          },
        ],
        en: [
          {
            displayedChars: 100,
            instruction: '* white: plug the duct to the purified air source',
            typing: false,
          },
          {
            displayedChars: 100,
            instruction: '* yellow: plug the duct to the half-purified air source',
            typing: false,
          },
          {
            displayedChars: 0,
            instruction: '* orange: plug the duct to the polluted air source polluted air source',
            typing: false,
          },
          {
            displayedChars: 0,
            instruction: '* blue: plug the duct to a more purified air source',
            typing: false,
          },
          {
            displayedChars: 0,
            instruction: '* pink: apply to this duct the sequence code of the previous duct',
            typing: false,
          },
          {
            displayedChars: 0,
            instruction: '* purple: apply to this duct the sequence code of the next duct',
            typing: false,
          },
        ],
      },
      unplugBeforeInterventionG: 255,
      unplugBeforeInterventionB: 255,
      continueHighlightingUnplugInstruction: true,
      unplugInstructionAnimation: null,
    }
  },
  computed: {
    highlightUnplugInstruction() {
      return progressionStore.state.highlightUnplugInstruction
    },
    unplugBeforeInterventionColor() {
      return "rgba(255, " + this.unplugBeforeInterventionG + ", " + this.unplugBeforeInterventionB + ", 1)"
    },
    terminalTop() {
      if (progressionStore.state.showDocumentation) {
        return "-1px"
      } else {
        return "-100%"
      }
    },
    getEscaped() {
      return function(string) {
        return string.replace(/ /g, "&nbsp;")
      }
    },
    displayedInstructions() {
      return this.colorInstructions[this.$i18n.locale]
    },
    puzzleRound() {
      return progressionStore.state.round
    },
  },
  methods: {
    typeOneChar(lang, instructionIndex) {
      this.colorInstructions[lang][instructionIndex].typing = true

      if (this.colorInstructions[lang][instructionIndex].displayedChars >= this.colorInstructions[lang][instructionIndex].instruction.length) {
        setTimeout(this.stopTyping, 425, lang, instructionIndex)
        if (this.typing[lang].queue.length > 0) {
          let nextInstructionIndex = this.typing[lang].queue.shift()
          this.typing[lang].task = setTimeout(this.typeOneChar, 425, lang, nextInstructionIndex)
        } else {
          this.typing[lang].task = null
        }
      } else {
        this.colorInstructions[lang][instructionIndex].displayedChars += 1
        this.typing[lang].task = setTimeout(this.typeOneChar, 75, lang, instructionIndex)
      }
    },
    stopTyping(lang, instructionIndex) {
      this.colorInstructions[lang][instructionIndex].typing = false
    },
  },
  watch: {
    highlightUnplugInstruction(newValue) {
      if (newValue) {
        this.continueHighlightingUnplugInstruction = true
        this.unplugInstructionAnimation.play()
      } else {
        this.continueHighlightingUnplugInstruction = false
      }
    },
    puzzleRound(newValue) {
      var lang
      if (newValue === 1) {
        for (lang of ["fr", "en"]) {
          if (this.typing[lang].task === null) {
            this.typeOneChar(lang, 2)
          } else {
            this.typing[lang].queue.push(2)
          }

          this.typing[lang].queue.push(3)
          this.typing[lang].queue.push(4)
        }
      } else if (newValue === 2) {
        for (lang of ["fr", "en"]) {
          if (this.typing[lang].task === null) {
            this.typeOneChar(lang, [5])
          } else {
            this.typing[lang].queue.push(5)
          }
        }
      } else {
        this.typingQueue = []
        clearTimeout(this.typingTask)
        for (lang of ["fr", "en"]) {
          for (var i = 2 ; i < this.colorInstructions[lang].length ; i++) {
            this.colorInstructions[lang][i].displayedChars = 0
            this.colorInstructions[lang][i].typing = false
          }
        }
      }
    },
  },
  created() {
    this.$anime({
      targets: this,
      underscoreOpacity: 1,
      duration: 500,
      loop: true,
      direction: 'alternate',
      easing: 'easeInOutExpo',
    })

    let this_ = this

    this.unplugInstructionAnimation = this.$anime({
      targets: this,
      unplugBeforeInterventionG: 0,
      unplugBeforeInterventionB: 0,
      autoplay: false,
      loop: true,
      direction: 'alternate',
      duration: 800,
      loopComplete: function(anim) {
        if (!this_.continueHighlightingUnplugInstruction && anim.progress === 0) {
          this_.unplugInstructionAnimation.pause()
        }
      },
      easing: 'easeInOutSine',
    })
  },
}
</script>

<style scoped>
.documentation {
  color: rgb(253, 246, 227);
  width: 90%;
  height: 70%;
  background-color: rgba(15, 30, 35, 0.96);
  font-family: "Monospace";
  left: 5%;
  transition: top 800ms ease-in-out;
}

.menu-line {
  background: rgba(253, 246, 227, 1);
  background: linear-gradient(
    0deg,
    rgba(253, 246, 227, 1),
    rgba(190, 210, 210, 1),
    rgba(253, 246, 227, 1)
  );
  color: rgb(15, 30, 35);
  font-weight: bold;
  font-family: "Nimbus Sans";
  font-size: 14px;
  clip-path: polygon(
    0% 0%,
    100% 0%,
    100% calc(100% - 5px),
    calc(100% - 5px) 100%,
    5px 100%,
    0px calc(100% - 5px)
  );
}

.border-white {
  border: 1px solid rgb(253, 246, 227);
  line-height: 1;
}

.border-right-thick {
  border-right-width: 2px;
}

.border-left-thick {
  border-left-width: 2px;
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

.bottom-right {
  bottom: 32px;
  right: 20px;
}

.button-reduce {
  border: 1px solid rgb(15, 30, 35);
  border-radius: 2px;
  line-height: 1;
  padding: 2px 2px 0px 2px;
}

.text-yellow {
  color: var(--yellow);
}

.text-orange {
  color: var(--orange);
}

.text-green {
  color: var(--green);
}

.text-teal {
  color: var(--teal);
}
</style>