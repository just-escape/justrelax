<template>
  <div class="d-flex justify-content-between align-items-center">
    <div class="text-one-line-ellipsis min-width-100px">{{ row.name }}</div>

    <b-button-group>
      <ButtonJaffa
        size="sm"
        v-for="(button, index) in row.widget_params.filter(b => isInMaintenanceMode || !b.maintenance)"
        :key="index"
        @click="click(button)"
        :title="button.help"
      >
        <!-- title is undefined, so does not exist in case help is not defined -->
        <i :class="button.icon"></i>
      </ButtonJaffa>
    </b-button-group>
  </div>
</template>

<script>
import ButtonJaffa from "@/components/common/ButtonJaffa.vue"
import roomStore from "@/store/roomStore.js"
import preferenceStore from '@/store/preferenceStore.js'

export default {
  name: "WidgetButtonsList",
  components: {
    ButtonJaffa,
  },
  computed: {
    isInMaintenanceMode() {
      return preferenceStore.state.isInMaintenanceMode
    },
  },
  methods: {
    click(button) {
      roomStore.dispatch('widgetAction', {channel: this.defaultChannel, widgetId: button.id, widgetType: 'button', action: "click", ...button.extra})
    }
  },
  props: [
    "defaultChannel",
    "row",
  ]
}
</script>
