<template>
  <b-card class="bgc-dark border-jaffa h-100" no-body>
    <b-card-header>
      <div class="d-flex flex-row justify-content-between align-items-center text-jaffa">
        <div>
        </div>
        <h3 class="big-noodle text-center mb-0">
          {{ card.name }}
        </h3>
        <div>
          <CollapseChevron class="align-self-center" v-b-toggle="'collapse-card-' + roomId + '-' + card.id"/>
        </div>
      </div>
    </b-card-header>

    <b-collapse :id="'collapse-card-' + roomId + '-' + card.id" :visible="true">
      <b-card-body>
        <div v-if="cardRows === undefined">
          Loading...
        </div>
        <ul v-else class="list-unstyled mb-0">
          <li v-for="(row, index) in cardRows.filter(cr => isInMaintenanceMode || !cr.maintenance)" :key="row.id" :class="{'mb-2': !isLastRow(index)}">
            <WidgetButtonsGroup v-if="row.widget === 'buttons_group'" :row="row" :defaultChannel="roomDefaultChannel"/>
            <WidgetSessionData v-if="row.widget === 'session_data'" :row="row" :defaultChannel="roomDefaultChannel" :roomId="roomId"/>
            <WidgetLogPrompt v-else-if="row.widget === 'log_prompt'" :row="row" :defaultChannel="roomDefaultChannel"/>
            <WidgetInstructionPrompt v-else-if="row.widget === 'instruction_prompt'" :row="row" :defaultChannel="roomDefaultChannel"/>
            <WidgetLasers v-else-if="row.widget === 'lasers'" :row="row" :defaultChannel="roomDefaultChannel" :roomId="roomId"/>
            <WidgetWaffleFactory v-else-if="row.widget === 'waffle_factory'" :row="row" :defaultChannel="roomDefaultChannel"/>
            <WidgetSynchronizerLights v-else-if="row.widget === 'synchronizer_lights'" :row="row" :defaultChannel="roomDefaultChannel" :roomId="roomId"/>
            <WidgetTextArea v-else-if="row.widget === 'textarea'" :row="row" :defaultChannel="roomDefaultChannel"/>
            <WidgetNodeRegister v-else-if="row.widget === 'node_register'" :row="row" :defaultChannel="roomDefaultChannel" :roomId="roomId"/>
            <WidgetChopsticks v-else-if="row.widget === 'chopsticks'" :row="row" :defaultChannel="roomDefaultChannel" :roomId="roomId"/>
            <WidgetTimer v-else-if="row.widget === 'timer'" :row="row" :defaultChannel="roomDefaultChannel" :roomId="roomId"/>
            <WidgetControlPanel v-else-if="row.widget === 'control_panel'" :row="row" :defaultChannel="roomDefaultChannel" :roomId="roomId"/>
            <WidgetSokoban v-else-if="row.widget === 'sokoban'" :row="row" :defaultChannel="roomDefaultChannel" :roomId="roomId"/>
            <WidgetRootServer v-else-if="row.widget === 'root_server'" :row="row" :defaultChannel="roomDefaultChannel" :roomId="roomId"/>
            <WidgetSynchronizer v-else-if="row.widget === 'synchronizer'" :row="row" :defaultChannel="roomDefaultChannel" :roomId="roomId"/>
          </li>
        </ul>
      </b-card-body>
    </b-collapse>
  </b-card>
</template>

<script>
import WidgetButtonsGroup from "@/components/live/WidgetButtonsGroup.vue"
import WidgetSessionData from "@/components/live/WidgetSessionData.vue"
import WidgetLogPrompt from "@/components/live/WidgetLogPrompt.vue"
import WidgetInstructionPrompt from "@/components/live/WidgetInstructionPrompt.vue"
import WidgetLasers from "@/components/live/WidgetLasers.vue"
import WidgetWaffleFactory from "@/components/live/WidgetWaffleFactory.vue"
import WidgetSynchronizerLights from "@/components/live/WidgetSynchronizerLights.vue"
import WidgetTextArea from "@/components/live/WidgetTextArea.vue"
import WidgetNodeRegister from "@/components/live/WidgetNodeRegister.vue"
import WidgetChopsticks from "@/components/live/WidgetChopsticks.vue"
import WidgetControlPanel from "@/components/live/WidgetControlPanel.vue"
import WidgetTimer from "@/components/live/WidgetTimer.vue"
import WidgetSokoban from "@/components/live/WidgetSokoban.vue"
import WidgetRootServer from "@/components/live/WidgetRootServer.vue"
import WidgetSynchronizer from "@/components/live/WidgetSynchronizer.vue"
import CollapseChevron from '@/components/common/CollapseChevron.vue'
import roomStore from "@/store/roomStore.js"
import notificationStore from '@/store/notificationStore.js'
import preferenceStore from '@/store/preferenceStore.js'

export default {
  name: "ActionCard",
  components: {
    WidgetButtonsGroup,
    WidgetSessionData,
    WidgetLogPrompt,
    WidgetInstructionPrompt,
    WidgetLasers,
    WidgetWaffleFactory,
    WidgetSynchronizerLights,
    WidgetTextArea,
    WidgetNodeRegister,
    WidgetChopsticks,
    WidgetControlPanel,
    WidgetTimer,
    CollapseChevron,
    WidgetSokoban,
    WidgetRootServer,
    WidgetSynchronizer,
  },
  data() {
    return {
      cardRows: undefined,
    }
  },
  computed: {
    isInMaintenanceMode() {
      return preferenceStore.state.isInMaintenanceMode
    },
    roomDefaultChannel() {
      for (let room of roomStore.state.rooms) {
        if (room.id === this.roomId) {
          return room.default_publication_channel
        }
      }

      // Can never happen, because roomStore.state.rooms is always defined if this component exist
      // This return statement just fixes a Vue compilation error
      return 'default_channel'
    },
  },
  methods: {
    isLastRow (index) {
      return index === Object.keys(this.cardRows).length - 1
    },
  },
  mounted() {
    let this_ = this
    this.$justRestAPI.get('/card_row/?card=' + this.card.id)
      .then(function (response) {
        this_.cardRows = response.data
      })
      .catch(function (error) {
        notificationStore.dispatch('pushError', 'Error while fetching card rows: ' + error)
      })
  },
  props: ["roomId", "card"]
}
</script>
