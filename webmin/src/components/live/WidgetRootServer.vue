<template>
  <div class="border-deepdark rounded p-3 mb-3">
    <div class="d-flex justify-content-between align-items-center">
        <div class="text-one-line-ellipsis min-width-100px mb-1">Interface simplifiée</div>
        <div
            v-if="getData('root_server_simplified_ui') !== undefined"
            class="border mr-1 position-relative pointer"
            style="border-color: #ef8649 !important; height: 17px; width: 17px"
            @click="setData('root_server_simplified_ui', !getData('root_server_simplified_ui'))"
        >
            <i v-if="getData('root_server_simplified_ui')" class="position-absolute text-jaffa fa fa-xs fa-fw fa-check" style="bottom: 0; right: 0"></i>
        </div>
    </div>
    <div class="d-flex justify-content-between align-items-center">
        <div class="text-one-line-ellipsis min-width-100px mb-1">Pulse sur VÉRIFIER</div>
        <div
            v-if="getData('root_server_pulsate_check_availability_button') !== undefined"
            class="border mr-1 position-relative pointer"
            style="border-color: #ef8649 !important; height: 17px; width: 17px"
            @click="setData('root_server_pulsate_check_availability_button', !getData('root_server_pulsate_check_availability_button'))"
        >
            <i v-if="getData('root_server_pulsate_check_availability_button')" class="position-absolute text-jaffa fa fa-xs fa-fw fa-check" style="bottom: 0; right: 0"></i>
        </div>
    </div>
    <div class="d-flex justify-content-between align-items-center">
        <div class="text-one-line-ellipsis min-width-100px mb-1">Afficher les ingrédients</div>
        <div
            v-if="getData('root_server_display_ingredients') !== undefined"
            class="border mr-1 position-relative pointer"
            style="border-color: #ef8649 !important; height: 17px; width: 17px"
            @click="setData('root_server_display_ingredients', !getData('root_server_display_ingredients'))"
        >
            <i v-if="getData('root_server_display_ingredients')" class="position-absolute text-jaffa fa fa-xs fa-fw fa-check" style="bottom: 0; right: 0"></i>
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
      return (key) => { return roomStore.state.sessionData[this.roomId][key] }
    },
  },
  methods: {
    setData(key, value) {
      roomStore.dispatch('widgetAction', {
        channel: this.defaultChannel,
        widgetId: 'root_server',
        widgetType: 'root_server',
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