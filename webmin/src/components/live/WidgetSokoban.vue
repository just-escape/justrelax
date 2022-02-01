<template>
  <div>
    <div class="d-flex flex-row justify-content-between">
      <MiniSokoban :currentFace="currentFace" :currentLevel="currentLevel" class="d-none"/>

      <div>Difficulté</div>

      <b-button-group>
        <ButtonJaffa
          size="sm" @click="setDifficulty('easy')"
          :active="difficulty === 'easy'"
          :disabled="lockDifficulty"
        >
          <i class="fa fa-fw fa-dice-one"></i>
        </ButtonJaffa>
        <ButtonJaffa
          size="sm" @click="setDifficulty('normal')"
          :active="difficulty === 'normal'"
          :disabled="lockDifficulty"
        >
          <i class="fa fa-fw fa-dice-two"></i>
        </ButtonJaffa>
        <ButtonJaffa
          size="sm" @click="setDifficulty('hard')"
          :active="difficulty === 'hard'"
          :disabled="lockDifficulty"
        >
          <i class="fa fa-fw fa-dice-three"></i>
        </ButtonJaffa>
      </b-button-group>
    </div>

    <div>Aides</div>
    <div v-for="(orderQueue, oqIndex) in orderQueues[difficulty]" :key="oqIndex">
      <div class="d-flex justify-content-between align-items-center mb-2">
        <div class="d-flex flex-row">
          <ButtonJaffa class="mr-1" size="sm" @click="queueMoves(orderQueue.moves)">
            <i class="fas fa-fw fa-play"></i>
          </ButtonJaffa>
          <div class="text-one-line-ellipsis align-self-center" style="min-width: 60px">
            {{ orderQueue.name }}
          </div>
        </div>
        <div>
          <CollapseChevron class="align-self-center text-jaffa" v-b-toggle="'collapse-sokoban-sketch-' + difficulty + '-' + oqIndex"/>
        </div>
      </div>
      <b-collapse :id="'collapse-sokoban-sketch-' + difficulty + '-' + oqIndex" :visible="false">
        <div class="mb-3">
          <img :src="orderQueue.sketch" class="img-fluid">
        </div>
      </b-collapse>
    </div>

    <div class="text-right border-deepdark px-2 py-1 rounded">
      <div class="d-flex flex-row justify-content-between text-jaffa">
        <div class="d-flex flex-column" style="flex: 1 1 0"></div>
        <div class="d-flex flex-column" style="flex: 1 1 0">Win</div>
        <div class="d-flex flex-column" style="flex: 1 1 0">Sta</div>
        <div class="d-flex flex-column" style="flex: 1 1 0">Tot</div>
        <div class="d-flex flex-column" style="flex: 1 1 0">Mov</div>
      </div>
      <div class="d-flex flex-row">
        <div class="d-flex flex-column text-jaffa text-center" style="flex: 1 1 0">
          1
        </div>
        <div class="d-flex flex-column" style="flex: 1 1 0">
          <Clock :seconds="successTime0" :displayZero="true"/>
        </div>
        <div class="d-flex flex-column" style="flex: 1 1 0">
          <Clock :seconds="firstMoveTime0" :displayZero="true"/>
        </div>
        <div class="d-flex flex-column" style="flex: 1 1 0">
          {{ movesPerLevel ? movesPerLevel[0].total : '' }}
        </div>
        <div class="d-flex flex-column" style="flex: 1 1 0">
          {{ movesPerLevel ? movesPerLevel[0].sinceLastReset : '' }}
        </div>
      </div>
      <div class="d-flex flex-row">
        <div class="d-flex flex-column text-jaffa text-center" style="flex: 1 1 0">
          2
        </div>
        <div class="d-flex flex-column" style="flex: 1 1 0">
          <Clock :seconds="successTime1" :displayZero="true"/>
        </div>
        <div class="d-flex flex-column" style="flex: 1 1 0">
          <Clock :seconds="firstMoveTime1" :displayZero="true"/>
        </div>
        <div class="d-flex flex-column" style="flex: 1 1 0">
          {{ movesPerLevel ? movesPerLevel[1].total : '' }}
        </div>
        <div class="d-flex flex-column" style="flex: 1 1 0">
          {{ movesPerLevel ? movesPerLevel[1].sinceLastReset : '' }}
        </div>
      </div>
      <div class="d-flex flex-row">
        <div class="d-flex flex-column text-jaffa text-center" style="flex: 1 1 0">
          3
        </div>
        <div class="d-flex flex-column" style="flex: 1 1 0">
          <Clock :seconds="successTime2" :displayZero="true"/>
        </div>
        <div class="d-flex flex-column" style="flex: 1 1 0">
          <Clock :seconds="firstMoveTime2" :displayZero="true"/>
        </div>
        <div class="d-flex flex-column" style="flex: 1 1 0">
          {{ movesPerLevel ? movesPerLevel[2].total : '' }}
        </div>
        <div class="d-flex flex-column" style="flex: 1 1 0">
          {{ movesPerLevel ? movesPerLevel[2].sinceLastReset : '' }}
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import MiniSokoban from "@/components/live/MiniSokoban.vue"
import ButtonJaffa from "@/components/common/ButtonJaffa.vue"
import CollapseChevron from '@/components/common/CollapseChevron.vue'
import Clock from "@/components/common/Clock.vue"
import roomStore from "@/store/roomStore.js"

export default {
  name: "WidgetSokoban",
  components: {
    MiniSokoban,
    ButtonJaffa,
    CollapseChevron,
    Clock,
  },
  data() {
    return {
      orderQueues: {
        easy: [
          {
            name: '3.A',
            moves: ["reset", "left", "up", "up", "down", "down", "right", "right", "up", "up"],
            sketch: require('@/assets/sokoban/sokoban_easy_3a.jpg'),
          },
        ],
        normal: [
          {
            name: '2.A',
            moves: ["reset", "up", "right", "right", "left", "left", "down", "down", "right", "right"],
            sketch: require('@/assets/sokoban/sokoban_normal_2a.jpg'),
          },
          {
            name: '3.A',
            moves: ["reset", "right", "right", "up", "up", "left", "down", "up", "left"],
            sketch: require('@/assets/sokoban/sokoban_normal_3a.jpg'),
          },
          {
            name: '3.B',
            moves: ["reset", "right", "right", "up", "up", "left", "down", "up", "left", "up", "up", "left", "left", "down", "down", "right"],
            sketch: require('@/assets/sokoban/sokoban_normal_3b.jpg'),
          },
        ],
        hard: [
          {
            name: '2.A',
            moves: ["reset", "right", "right", "right", "right", "down", "down", "left", "up", "down", "left"],
            sketch: require('@/assets/sokoban/sokoban_hard_2a.jpg'),
          },
          {
            name: '2.B',
            moves: ["reset", "right", "right", "right", "right", "down", "down", "left", "up", "down", "left", "down", "down", "left", "left", "up", "up", "right"],
            sketch: require('@/assets/sokoban/sokoban_hard_2b.jpg'),
          },
          {
            name: '3.A',
            moves: ["reset", "left", "up", "up", "down", "down", "right", "right", "up", "up", "left", "left", "down", "left", "left", "up", "up", "up", "right", "right", "down"],
            sketch: require('@/assets/sokoban/sokoban_hard_3a.jpg'),
          },
          {
            name: '3.B',
            moves: ["reset", "left", "up", "up", "down", "down", "right", "right", "up", "up", "left", "left", "down", "left", "left", "up", "up", "up", "right", "right", "down", "down", "left", "right", "right", "right", "down", "down", "left", "left", "up"],
            sketch: require('@/assets/sokoban/sokoban_hard_3b.jpg'),
          },
          {
            name: '3.C',
            moves: ["reset", "left", "up", "up", "down", "down", "right", "right", "up", "up", "left", "left", "down", "left", "left", "up", "up", "up", "right", "right", "down", "down", "left", "right", "right", "right", "down", "down", "left", "left", "up", "down", "right", "right", "up", "up", "left", "left"],
            sketch: require('@/assets/sokoban/sokoban_hard_3c.jpg'),
          },
        ],
      }
    }
  },
  computed: {
    currentFace() {
      return roomStore.state.sessionData[this.roomId].sokoban_current_face
    },
    currentLevel() {
      return roomStore.state.sessionData[this.roomId].sokoban_current_level
    },
    difficulty() {
      return roomStore.state.sessionData[this.roomId].sokoban_difficulty
    },
    lockDifficulty() {
      return roomStore.state.sessionData[this.roomId].sokoban_lock_difficulty
    },
    marmitronPositions() {
      return roomStore.state.sessionData[this.roomId].sokoban_marmitron_positions
    },
    blocksPositions() {
      return roomStore.state.sessionData[this.roomId].sokoban_blocks_position
    },
    movesPerLevel() {
      return roomStore.state.sessionData[this.roomId].sokoban_moves_per_level
    },
    firstMoveTime0() {
      return roomStore.state.sessionData[this.roomId].sokoban_first_move_time_0
    },
    firstMoveTime1() {
      return roomStore.state.sessionData[this.roomId].sokoban_first_move_time_1
    },
    firstMoveTime2() {
      return roomStore.state.sessionData[this.roomId].sokoban_first_move_time_2
    },
    successTime0() {
      return roomStore.state.sessionData[this.roomId].sokoban_success_time_0
    },
    successTime1() {
      return roomStore.state.sessionData[this.roomId].sokoban_success_time_1
    },
    successTime2() {
      return roomStore.state.sessionData[this.roomId].sokoban_success_time_2
    },
    success() {
      return roomStore.state.sessionData[this.roomId].sokoban_success
    },
  },
  methods: {
    queueMoves(moves) {
      roomStore.dispatch(
        'widgetAction',
        {
          channel: this.defaultChannel,
          widgetId: "sokoban",
          widgetType: "sokoban",
          action: "queue_moves",
          moves: moves,
        }
      )
    },
    setDifficulty(difficulty) {
      roomStore.dispatch(
        'widgetAction',
        {
          channel: this.defaultChannel,
          widgetId: "sokoban",
          widgetType: "sokoban",
          action: "set_difficulty",
          difficulty: difficulty,
        }
      )
    }
  },
  props: [
    "defaultChannel",
    "row",
    "roomId",
  ]
}
</script>

<style scoped>
.separated-moves:nth-child(5n):not(:last-child) {
  margin-right: 5px;
}
</style>