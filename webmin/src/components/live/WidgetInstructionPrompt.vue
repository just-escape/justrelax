<template>
  <div class="d-flex flex-column min-width-100px">
    <div class="text-one-line-ellipsis mb-1">{{ row.name }}</div>
    <div class="d-flex flex-row mb-1">
      <div class="mr-2 w-100">
        <b-form-select class="form-control w-100" v-model="presetMessage" :options="row.widget_params.preset_messages"></b-form-select>
      </div>
      <ButtonJaffa size="sm" @click="sendPresetLog">
        <i class="fa-fw fas fa-terminal"></i>
      </ButtonJaffa>
    </div>
    <div class="d-flex flex-row mb-1">
      <b-input v-model="rawLog" class="mr-2" placeholder="instruction"></b-input>
      <ButtonJaffa size="sm" @click="sendLog">
        <i class="fa-fw fas fa-terminal"></i>
      </ButtonJaffa>
    </div>
  </div>
</template>

<script>
import ButtonJaffa from "@/components/common/ButtonJaffa.vue"
import roomStore from "@/store/roomStore.js"

export default {
  name: "WidgetInstructionPrompt",
  components: {
    ButtonJaffa,
  },
  data() {
    return {
      presetMessage: null,
      rawLog: '',
    }
  },
  methods: {
    sendPresetLog() {
      roomStore.dispatch('widgetAction', {
        channel: this.defaultChannel,
        widgetId: this.row.widget_params.id,
        widgetType: 'instruction_prompt',
        action: "send_log",
        use_locale: true,
        message: this.presetMessage.message,
        ...this.row.widget_params.extra
      })
    },
    sendLog() {
      roomStore.dispatch('widgetAction', {
        channel: this.defaultChannel,
        widgetId: this.row.widget_params.id,
        widgetType: 'instruction_prompt',
        action: "send_log",
        use_locale: false,
        message: this.rawLog,
        ...this.row.widget_params.extra
      })
    },
  },
  mounted() {
    this.presetMessage = this.row.widget_params.preset_messages[0].value
  },
  props: [
    "defaultChannel",
    "row",
  ]
}
</script>
