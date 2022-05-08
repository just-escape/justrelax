<template>
    <div class="w-100 border-deepdark rounded p-2 d-flex flex-column justify-content-around mb-2">
      <div class="mb-2">
      </div>

      <div v-if="getData('ventilation_panel_instructions')">
      <div
        v-for="(difficultyInstructionSets, round_) in getData('ventilation_panel_instructions')" :key="round_"
        :class="{'mb-1': round_ === 'round0' || round_ === 'round1'}"
      >
        <div v-if="round_ === 'round0'">Round 1</div>
        <div v-else-if="round_ === 'round1'">Round 2</div>
        <div v-else-if="round_ === 'round2'">Round 3</div>

        <div class="d-flex flex-row">
            <div
            class="d-flex flex-column"
            v-for="(difficultyInstructionSet, difficultyInstructionSetIndex) in difficultyInstructionSets" :key="difficultyInstructionSetIndex"
            >
                <div
                    v-for="(cycleSequenceSet, cycleSequenceSetIndex) in difficultyInstructionSet" :key="cycleSequenceSetIndex"
                    class="d-flex flex-row mr-2 pl-1 mb-1 rounded pointer"
                    :class="{
                        'border-jaffa': getInstructionSetIndex(round_) === cycleSequenceSetIndex && getDifficulty(round_) === difficultyInstructionSetIndex,
                        'border-deepdark': !(getInstructionSetIndex(round_) === cycleSequenceSetIndex && getDifficulty(round_) === difficultyInstructionSetIndex),
                    }"
                    @click="setRoundDifficulty(round_, difficultyInstructionSetIndex, cycleSequenceSetIndex)"
                >
                    <div v-for="(instruction, instructionIndex) in cycleSequenceSet" :key="instructionIndex" class="mr-1">
                        <div class="d-flex flex-column">
                            <div
                                class="rounded"
                                :style="{background: instruction.air_duct === 'ad0' ? instruction.color : 'black'}"
                                style="height: 8px; width: 8px; margin: 1px"
                            ></div>
                            <div
                                class="rounded"
                                :style="{background: instruction.air_duct === 'ad1' ? instruction.color : 'black'}"
                                style="height: 8px; width: 8px; margin: 1px"
                            ></div>
                            <div
                                class="rounded"
                                :style="{background: instruction.air_duct === 'ad2' ? instruction.color : 'black'}"
                                style="height: 8px; width: 8px; margin: 1px"
                            ></div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
      </div>
      </div>
    </div>
</template>

<script>
// import ButtonJaffa from "@/components/common/ButtonJaffa.vue"
import roomStore from "@/store/roomStore.js"

export default {
  name: "WidgetVentilationPanel",
  components: {
    // ButtonJaffa,
  },
  computed: {
    getData() {
      return (key) => { return roomStore.state.sessionData[this.roomId][key] }
    },
    getInstructionSetIndex() {
      return (round_) => {
          let roundIndex
          if (round_ === 'round1') {
              roundIndex = 1
          } else if (round_ === 'round2') {
              roundIndex = 2
          } else {
              roundIndex = 0
          }
          return this.getData('ventilation_panel_instruction_set_indexes')[roundIndex]
      }
    },
    getDifficulty() {
      return (round_) => {
          let roundIndex
          if (round_ === 'round1') {
              roundIndex = 1
          } else if (round_ === 'round2') {
              roundIndex = 2
          } else {
              roundIndex = 0
          }
          return this.getData('ventilation_panel_difficulties')[roundIndex]
      }
    },
  },
  methods: {
    reset() {
      roomStore.dispatch(
        'widgetAction',
        {
          channel: this.defaultChannel,
          widgetId: 'ventilation_panel',
          widgetType: 'ventilation_panel',
          action: "reset",
        }
      )
    },
    setRoundDifficulty(round_, difficultyIndex, instructionSetIndex) {
      let roundIndex
      if (round_ === 'round1') {
          roundIndex = 1
      } else if (round_ === 'round2') {
          roundIndex = 2
      } else {
          roundIndex = 0
      }
      roomStore.dispatch('widgetAction', {
        channel: this.defaultChannel,
        widgetId: 'ventilation_panel',
        widgetType: 'ventilation_panel',
        action: 'set_round_difficulty',
        round_: roundIndex,
        difficulty_index: difficultyIndex,
        instruction_set_index: instructionSetIndex,
      })
    },
    setData(key, value) {
      roomStore.dispatch('widgetAction', {
        channel: this.defaultChannel,
        widgetId: 'ventilation_panel',
        widgetType: 'ventilation_panel',
        action: 'set',
        key: key,
        value: value,
      })
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
.bg-red {
    background: red;
}
.bg-black {
    background: red;
}
</style>
