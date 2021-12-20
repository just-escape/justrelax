<template>
  <div class="d-flex flex-column min-width-100px">
    <div class="text-one-line-ellipsis mb-1">{{ row.name }}</div>
    <div class="d-flex flex-row mb-1">
      <div class="mr-2 w-100">
        <b-form-select class="form-control w-100" v-model="presetMessage" :options="presetMessagesOptions" :html="true"></b-form-select>
      </div>
      <ButtonJaffa size="sm" @click="sendPresetLog">
        <i class="fa-fw far fa-paper-plane"></i>
      </ButtonJaffa>
    </div>
    <div class="d-flex flex-row mb-1">
      <b-input v-model="rawLog" class="mr-2" placeholder="log"></b-input>
      <ButtonJaffa size="sm" class="mr-2" @click="sendLog('info')">
        <i class="fa-fw fas fa-info"></i>
      </ButtonJaffa>
      <ButtonJaffa size="sm" @click="sendLog('warning')">
        <i class="fa-fw fas fa-exclamation"></i>
      </ButtonJaffa>
    </div>
  </div>
</template>

<script>
import ButtonJaffa from "@/components/common/ButtonJaffa.vue"
import roomStore from "@/store/roomStore.js"

export default {
  name: "WidgetLogPrompt",
  components: {
    ButtonJaffa,
  },
  data() {
    return {
      presetMessage: null,
      rawLog: '',
    }
  },
  computed: {
    presetMessagesOptions() {
      let options = []
      for (let option of this.row.widget_params.preset_messages) {
        let text = option.text
        if (option.value.level == 'info') {
            text = '[i] ' + text
        } else if (option.value.level == 'warning') {
            text = '[!] ' + text
        }
        options.push({value: option.value, text: text})
      }
      return options
    },
  },
  methods: {
    sendPresetLog() {
      roomStore.dispatch('widgetAction', {
        channel: this.defaultChannel,
        widgetId: this.row.widget_params.id,
        widgetType: 'log_prompt',
        action: "send_log",
        use_locale: true,
        level: this.presetMessage.level,
        message: this.presetMessage.message,
        ...this.row.widget_params.extra
      })
    },
    sendLog(level) {
      roomStore.dispatch('widgetAction', {
        channel: this.defaultChannel,
        widgetId: this.row.widget_params.id,
        widgetType: 'log_prompt',
        action: "send_log",
        use_locale: false,
        level: level,
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