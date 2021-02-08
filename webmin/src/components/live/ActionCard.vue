<template>
  <b-card
    :header="card.name"
    header-tag="h3"
    header-class="big-noodle text-jaffa text-center"
    class="bgc-dark border-jaffa h-100"
  >
    <div v-if="cardRows === undefined">
      Loading...
    </div>
    <ul v-else class="list-unstyled mb-0">
      <li v-for="(row, index) in cardRows" :key="row.id" :class="{'mb-2': !isLastRow(index)}">
        <WidgetButtonsGroup v-if="row.widget === 'buttons_group'" :row="row" :defaultChannel="roomDefaultChannel"/>
      </li>
    </ul>
  </b-card>
</template>

<script>
import WidgetButtonsGroup from "@/components/live/WidgetButtonsGroup.vue"
import roomStore from "@/store/roomStore.js"
import notificationStore from '@/store/notificationStore.js'

export default {
  name: "ActionCard",
  components: {
    WidgetButtonsGroup,
  },
  data() {
    return {
      cardRows: undefined,
    }
  },
  computed: {
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
