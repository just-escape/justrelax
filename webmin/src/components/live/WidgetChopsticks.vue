<template>
  <div class="w-100">
    <div class="d-flex flex-row justify-content-between mb-2">
      <div>Difficulté</div>

      <b-button-group>
        <ButtonJaffa
          size="sm" @click="setDifficulty('easy')"
          :active="difficulty === 'easy'"
        >
          <i class="fa fa-fw fa-dice-one"></i>
        </ButtonJaffa>
        <ButtonJaffa
          size="sm" @click="setDifficulty('normal')"
          :active="difficulty === 'normal'"
        >
          <i class="fa fa-fw fa-dice-two"></i>
        </ButtonJaffa>
      </b-button-group>
    </div>
    <div class="border-deepdark rounded p-3 d-flex flex-row justify-content-around mb-2">
        <div class="d-flex flex-column">
            <div style="height: 24px">
                <div class="chopstick-hole pointer" @click="toggleLetter(0)"></div>
            </div>
            <div style="height: 24px">
                <div class="chopstick-hole pointer" @click="toggleLetter(1)"></div>
            </div>
            <div style="height: 24px">
                <div class="chopstick-hole pointer" @click="toggleLetter(2)"></div>
            </div>
            <div style="height: 24px">
                <div class="chopstick-hole pointer" @click="toggleLetter(3)"></div>
            </div>
            <div style="height: 24px">
                <div class="chopstick-hole pointer" @click="toggleLetter(4)"></div>
            </div>
            <div style="height: 24px">
                <div class="chopstick-hole pointer" @click="toggleLetter(5)"></div>
            </div>
            <div style="height: 24px">
                <div class="chopstick-hole pointer" @click="toggleLetter(6)"></div>
            </div>
        </div>
        <div class="d-flex flex-column">
            <div class="text-primary">C</div>
            <div class="text-jaffa">O<span v-if="difficulty === 'normal'">*</span></div>
            <div class="text-jaffa">N<span v-if="difficulty === 'normal'">*</span></div>
            <div class="text-jaffa">T</div>
            <div class="text-jaffa">R<span v-if="difficulty === 'normal'">*</span></div>
            <div class="text-jaffa">O<span v-if="difficulty === 'normal'">*</span></div>
            <div class="text-jaffa">L</div>
        </div>
        <div class="d-flex flex-column">
            <div
                v-for="(color, colorIndex) in colors" :key="colorIndex"
                style="height: 24px"
            >
                <div
                  :style="{background: color == 'blue' ? 'var(--primary)' : '#f38d40'}"
                  class="chopsticks-color"
                ></div>
            </div>
        </div>
    </div>
    <div class="d-flex flex-row justify-content-end mb-2">
      <b-button-group>
        <ButtonJaffa
          size="sm"
          @click="forceSuccess"
        >
          <i class="fa fa-fw fa-check"></i>
        </ButtonJaffa>
        <ButtonJaffa
          size="sm"
          @click="reset"
        >
          <i class="fa fa-fw fa-undo-alt"></i>
        </ButtonJaffa>
      </b-button-group>
    </div>
    <div class="text-right border-deepdark px-2 py-1 rounded">
        <div class="d-flex flex-row justify-content-between text-jaffa">
            <div class="d-flex flex-column" style="flex: 1 1 0">Succès</div>
            <div class="d-flex flex-column" style="flex: 1 1 0">1er coup</div>
            <div class="d-flex flex-column" style="flex: 1 1 0">Nb coups</div>
        </div>
        <div class="d-flex flex-row">
            <div class="d-flex flex-column" style="flex: 1 1 0">
                <Clock :seconds="successTime" :displayZero="true"/>
            </div>
            <div class="d-flex flex-column" style="flex: 1 1 0">
                <Clock :seconds="firstMoveTime" :displayZero="true"/>
            </div>
            <div class="d-flex flex-column" style="flex: 1 1 0">
                {{ nMoves }}
            </div>
        </div>
    </div>
  </div>
</template>

<script>
import Clock from "@/components/common/Clock.vue"
import ButtonJaffa from "@/components/common/ButtonJaffa.vue"
import roomStore from "@/store/roomStore.js"

export default {
  name: "WidgetChopsticks",
  components: {
    Clock,
    ButtonJaffa,
  },
  data() {
    return {
      pluggedLetters: [false, false, false, false, false, false, false]
    }
  },
  methods: {
    toggleLetter(letterIndex) {
      let action = "emulate_chopstick_plug"
      if (this.difficulty === 'normal') {
        if ([1, 2, 4, 5].includes(letterIndex)) {
          if (this.pluggedLetters[letterIndex]) {
            action = "emulate_chopstick_unplug"
          }
          this.pluggedLetters[letterIndex] = !this.pluggedLetters[letterIndex]
        }
      }

      roomStore.dispatch(
        'widgetAction',
        {
          channel: this.defaultChannel,
          widgetId: 'chopsticks',
          widgetType: 'chopsticks',
          action: action,
          letter_index: letterIndex,
        }
      )
    },
    forceSuccess() {
      roomStore.dispatch(
        'widgetAction',
        {
          channel: this.defaultChannel,
          widgetId: 'chopsticks',
          widgetType: 'chopsticks',
          action: "force_success",
        }
      )
    },
    reset() {
      roomStore.dispatch(
        'widgetAction',
        {
          channel: this.defaultChannel,
          widgetId: 'chopsticks',
          widgetType: 'chopsticks',
          action: "reset",
        }
      )
    },
    setDifficulty(difficulty) {
      roomStore.dispatch(
        'widgetAction',
        {
          channel: this.defaultChannel,
          widgetId: "chopsticks",
          widgetType: "chopsticks",
          action: "set_difficulty",
          difficulty: difficulty,
        }
      )
    }
  },
  computed: {
    difficulty() {
      return roomStore.state.sessionData[this.roomId].chopsticks_difficulty
    },
    successTime() {
      return roomStore.state.sessionData[this.roomId].chopsticks_success_time
    },
    firstMoveTime() {
      return roomStore.state.sessionData[this.roomId].chopsticks_first_move_time
    },
    nMoves() {
      return roomStore.state.sessionData[this.roomId].chopsticks_moves
    },
    colors() {
      return roomStore.state.sessionData[this.roomId].chopsticks_colors
    },
  },
  props: [
    "defaultChannel",
    "row",
    "roomId",
  ]
}
</script>

<style scoped>
.chopstick-hole {
    width: 20px;
    height: 20px;
    border-radius: 50%;
    border: 6px #2e2e2e solid;
    background: lightgrey;
}

.chopsticks-color {
    width: 20px;
    height: 20px;
    border-radius: 50%;
}
</style>