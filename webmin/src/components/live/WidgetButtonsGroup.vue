<template>
  <div class="d-flex justify-content-between align-items-center">
    <div class="text-one-line-ellipsis min-width-100px">{{ row.name }}</div>

    <b-button-group>
      <ButtonJaffa
        size="sm"
        v-for="button in row.widget_params"
        :key="button.id"
        @click="click(button)"
      >
        <i :class="button.icon"></i>
      </ButtonJaffa>
    </b-button-group>
  </div>
</template>

<script>
import ButtonJaffa from "@/components/common/ButtonJaffa.vue"
import roomStore from "@/store/roomStore.js"

export default {
  name: "WidgetButtonsList",
  components: {
    ButtonJaffa,
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

<style scoped>
.min-width-100px {
  min-width: 100px;
}
</style>