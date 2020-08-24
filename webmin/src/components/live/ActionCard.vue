<template>
  <b-card
    :header="card.name"
    header-tag="h3"
    header-class="big-noodle text-jaffa text-center"
    class="bgc-dark border-jaffa h-100"
  >
    <ul v-if="displayRows" class="list-unstyled mb-0">
      <li v-for="(row, index) in card.rows" :key="row.id" :class="{'mb-2': !isLastRow(index)}">
        <WidgetButtonsGroup v-if="row.widget === 'buttons_group'" :row="row" :roomId="roomId"/>
      </li>
    </ul>
  </b-card>
</template>

<script>
import WidgetButtonsGroup from "@/components/live/WidgetButtonsGroup.vue"
import roomStore from "@/store/roomStore.js"

export default {
  name: "ActionCard",
  components: {
    WidgetButtonsGroup,
  },
  computed: {
    displayRows() {
      return this.card.rows !== undefined
    },
  },
  methods: {
    isLastRow (index) {
      return index === Object.keys(this.card.rows).length - 1
    },
  },
  created() {
    roomStore.dispatch("fetchCardRows", {
      roomId: this.roomId,
      cardId: this.card.id
    })
  },
  props: ["roomId", "card"]
}
</script>
