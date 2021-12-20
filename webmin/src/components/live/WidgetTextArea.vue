<template>
  <div class="d-flex flex-column min-width-100px">
    <div class="text-one-line-ellipsis mb-1">{{ row.name }}</div>
    <div class="d-flex flex-row mb-1">
      <b-textarea v-model="value" class="mr-2" rows="3"></b-textarea>
      <ButtonJaffa size="sm" @click="push">
        <i class="fa-fw fas fa-paper-plane"></i>
      </ButtonJaffa>
    </div>
  </div>
</template>

<script>
import ButtonJaffa from "@/components/common/ButtonJaffa.vue"
import roomStore from "@/store/roomStore.js"

export default {
  name: "WidgetTextArea",
  components: {
    ButtonJaffa,
  },
  data() {
    return {
      value: '',
    }
  },
  methods: {
    push() {
      roomStore.dispatch('widgetAction', {
        channel: this.defaultChannel,
        widgetId: this.row.widget_params.id,
        widgetType: 'textarea',
        action: "push",
        value: this.value,
        ...this.row.widget_params.extra
      })
    },
  },
  props: [
    "defaultChannel",
    "row",
  ]
}
</script>