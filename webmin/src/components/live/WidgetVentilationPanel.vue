<template>
    <div class="w-100 border-deepdark rounded p-2 d-flex flex-column justify-content-around mb-2">
      <div class="d-flex justify-content-between align-items-center mb-2">
        <div class="text-one-line-ellipsis min-width-100px">Lancer les instructions</div>
          <ButtonJaffa size="sm" @click="restartRound">
            <i class="fa fa-fw fa-play"></i>
          </ButtonJaffa>
      </div>

    <div class="d-flex flex-row justify-content-between mb-2">
      <div>Status</div>

      <b-button-group>
        <ButtonJaffa
          size="sm" @click="setStatus('inactive')"
          :active="status === 'inactive'"
        >
          <i class="fa fa-fw fa-lock"></i>
        </ButtonJaffa>
        <ButtonJaffa
          size="sm" @click="setStatus('playing')"
          :active="status === 'playing'"
        >
          <i class="fa fa-fw fa-gamepad"></i>
        </ButtonJaffa>
        <ButtonJaffa
          size="sm" @click="setStatus('success')"
          :active="status === 'success'"
        >
          <i class="fa fa-fw fa-check"></i>
        </ButtonJaffa>
      </b-button-group>
    </div>

      <div class="d-flex flex-row mb-3 justify-content-between">
        <div class="d-flex flex-row border-deepdark rounded p-1 mr-3">
          <div class="d-flex flex-column mr-4">
            <div
              :style="{background: getAirDuctColor('ad0')}"
              style="border-radius: 50%; height: 20px; width: 20px"
              class="mb-3"
              :class="{loading: getData('ventilation_panel_is_sequence_being_displayed')}"
            ></div>
            <div
              :style="{background: getAirDuctColor('ad1')}"
              style="border-radius: 50%; background: getAirDuctColor('ad1'); height: 20px; width: 20px"
              class="mb-3"
              :class="{loading: getData('ventilation_panel_is_sequence_being_displayed')}"
            ></div>
            <div
              :style="{background: getAirDuctColor('ad2')}"
              style="border-radius: 50%; background: getAirDuctColor('ad2'); height: 20px; width: 20px"
              :class="{loading: getData('ventilation_panel_is_sequence_being_displayed')}"
            ></div>
          </div>
          <div class="d-flex flex-column">
            <div
              style="border-radius: 50%; background: white; height: 20px; width: 20px"
              class="mb-3"
            ></div>
            <div
              style="border-radius: 50%; background: yellow; height: 20px; width: 20px"
              class="mb-3"
            ></div>
            <div
              style="border-radius: 50%; background: orange; height: 20px; width: 20px"
            ></div>
          </div>
        </div>

        <div
            class="d-flex flex-row rounded pointer border-deepdark p-1"
            v-if="getData('ventilation_panel_success_sequence') && getData('ventilation_panel_success_sequence').length > 0"
        >
            <div v-for="(instruction, instructionIndex) in getData('ventilation_panel_success_sequence')" :key="instructionIndex">
                <div
                  class="d-flex flex-column rounded"
                  :class="{
                    'mr-2': instructionIndex < getData('ventilation_panel_success_sequence').length - 1,
                    'border-jaffa': getData('ventilation_panel_sequence_cursor') === instructionIndex,
                    'border-transparent': getData('ventilation_panel_sequence_cursor') !== instructionIndex,
                  }"
                >
                    <div
                        class="mb-3"
                        :style="{background: instruction.air_duct === 'ad0' ? instruction.color : 'black'}"
                        style="border-radius: 50%; height: 20px; width: 20px"
                    ></div>
                    <div
                        class="mb-3"
                        :style="{background: instruction.air_duct === 'ad1' ? instruction.color : 'black'}"
                        style="border-radius: 50%; height: 20px; width: 20px"
                    ></div>
                    <div
                        :style="{background: instruction.air_duct === 'ad2' ? instruction.color : 'black'}"
                        style="border-radius: 50%; height: 20px; width: 20px"
                    ></div>
                </div>
            </div>
        </div>
      </div>

      <div v-if="getData('ventilation_panel_instructions')">
      <div
        v-for="(difficultyInstructionSets, round_) in getData('ventilation_panel_instructions')" :key="round_"
        :class="{'mb-1': round_ === 'round0' || round_ === 'round1'}"
      >
        <div v-if="round_ === 'round0'">Round 1{{getRoundTry('0')}}</div>
        <div v-else-if="round_ === 'round1'">Round 2{{getRoundTry('1')}}</div>
        <div v-else-if="round_ === 'round2'">Round 3{{getRoundTry('2')}}</div>

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
import ButtonJaffa from "@/components/common/ButtonJaffa.vue"
import roomStore from "@/store/roomStore.js"

export default {
  name: "WidgetVentilationPanel",
  components: {
    ButtonJaffa,
  },
  computed: {
    getData() {
      return (key) => { return roomStore.state.sessionData[this.roomId][key] }
    },
    getRoundTry() {
      return (round) => {
        let tryCounters = this.getData('ventilation_panel_try_counters')
        if (!tryCounters) {
          return ''
        }

        if (!tryCounters[round]) {
          return ''
        } else {
          return ' - ' + tryCounters[round] + ' essai(s)'
        }
      }
    },
    getAirDuctColor() {
      return (ductName) => {
        let airSources = this.getData('ventilation_panel_air_ducts')
        let sequenceCursor = this.getData('ventilation_panel_sequence_cursor')
        if (!airSources) {
          return 'black'
        }

        let connection = airSources[ductName]

        if (connection === 'as0') {
          return sequenceCursor == -1 ? 'red' : 'white'
        } else if (connection === 'as1') {
          return sequenceCursor == -1 ? 'red' : 'yellow'
        } else if (connection === 'as2') {
          return sequenceCursor == -1 ? 'red' : 'orange'
        } else {
          return 'black'
        }
      }
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
    status() {
      return this.getData('ventilation_panel_status')
    },
  },
  methods: {
    setStatus(status) {
      roomStore.dispatch(
        'widgetAction',
        {
          channel: this.defaultChannel,
          widgetId: 'ventilation_panel',
          widgetType: 'ventilation_panel',
          action: "set_status",
          status: status,
        }
      )
    },
    restartRound() {
      roomStore.dispatch(
        'widgetAction',
        {
          channel: this.defaultChannel,
          widgetId: 'ventilation_panel',
          widgetType: 'ventilation_panel',
          action: "restart_round",
        }
      )
    },
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
.loading {
  display: inline-block;
  width: 20px;
  height: 20px;
  border: 4px solid white;
  border-radius: 50%;
  border-top-color: black;
  animation: spin 1s ease-in-out infinite;
}

@keyframes spin {
  to { -webkit-transform: rotate(360deg); }
}
</style>
