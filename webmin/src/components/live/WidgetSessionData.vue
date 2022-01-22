<template>
  <div class="d-flex justify-content-between align-items-center">
    <div class="text-one-line-ellipsis min-width-100px mb-1">{{ row.name }}</div>
    <div v-if="row.widget_params.widget === 'checkbox'">
      <div
        v-if="getData !== undefined"
        class="border mr-1 position-relative pointer"
        style="border-color: #ef8649 !important; height: 17px; width: 17px"
        @click="setData(!getData)"
      >
        <i v-if="getData" class="position-absolute text-jaffa fa fa-xs fa-fw fa-check" style="bottom: 0; right: 0"></i>
      </div>
    </div>
    <div v-else-if="row.widget_params.widget === 'input_device'">
      <div
        v-if="getData !== undefined"
        class="border mr-1 position-relative"
        style="border-color: #ef8649 !important; height: 17px; width: 17px"
      >
        <i v-if="getData" class="position-absolute text-jaffa fa fa-xs fa-fw fa-check" style="bottom: 0; right: 0"></i>
      </div>
    </div>
  </div>
</template>

<script>
import roomStore from "@/store/roomStore.js"

export default {
  name: "WidgetSessionData",
  computed: {
    getData() {
      return roomStore.state.sessionData[this.roomId][this.row.widget_params.key]
    },
  },
  methods: {
    setData(value) {
      roomStore.dispatch('widgetAction', {
        channel: this.defaultChannel,
        widgetId: this.row.widget_params.key,
        widgetType: 'session_data',
        action: 'set',
        key: this.row.widget_params.key,
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