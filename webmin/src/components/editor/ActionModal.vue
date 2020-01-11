<template>
  <b-modal
    :id="modalId"
    body-bg-variant="dark"
    body-text-variant="light"
    @ok="ok"
    @hidden="hidden"
  >
    <select v-model="selected" class="mr-2">
      <option disabled value="">Choose</option>
      <option v-for="(value, key) in options" :key="key" :value="key">{{ value }}</option>
    </select>

    <div v-if="tmpAction.name == 'switch_yellow_led_on'">
      Send message
        <Argument
          v-b-modal="getSubmodalId('message')"
          :argument="tmpAction.message"
          :editable="true"
          :lastEdited="lastEditedArgument == 'message'"
        />
      to node named
        <Argument
          v-b-modal="getSubmodalId('node_name')"
          :argument="tmpAction.node_name"
          :editable="true"
          :lastEdited="lastEditedArgument == 'node_name'"
        />

      <ArgumentModal
        :modalId="getSubmodalId('message')"
        :argument="tmpAction.message"
        @updateArgument="(argument) => updateArgument('message', argument)"
        @hidden="updateLastEditedArgument('message')"
      />
      <ArgumentModal
        :modalId="getSubmodalId('node_name')"
        :argument="tmpAction.node_name"
        @updateArgument="(argument) => updateArgument('node_name', argument)"
        @hidden="updateLastEditedArgument('node_name')"
      />
    </div>
    <div v-else-if="tmpAction.name == 'cancel_red_and_green_led_hint_alarm'">
      Action 2
    </div>
    <div v-else-if="tmpAction.name == 'action 3'">
      Action 3
    </div>
    <div v-else-if="tmpAction.name == 'action 4'">
      Action 4
    </div>
  </b-modal>
</template>

<script>
import Argument from '@/components/editor/Argument.vue'
import ArgumentModal from '@/components/editor/ArgumentModal.vue'

export default {
  name: "ActionModal",
  components: {
    Argument,
    ArgumentModal,
  },
  data() {
    return {
      tmpAction: {},
      options: {
        'switch_yellow_led_on': 'Action 1',
        'cancel_red_and_green_led_hint_alarm': 'Action 2',
        'action 3': 'Action 3',
        'action 4': 'Action 4',
      },
      lastEditedArgument: null,
    }
  },
  computed: {
    selected: {
      get() {
        return this.tmpAction.name
      },
      set(value) {
        if (this.tmpAction.name == value) {
          return
        }

        this.tmpAction.name = value
        delete this.tmpAction.message
        delete this.tmpAction.node_name
        this.lastEditedArgument = null

        if (this.tmpAction.name == 'switch_yellow_led_on') {
          this.tmpAction.message = 'hello'
          this.tmpAction.node_name = 'node'
        }
      }
    }
  },
  methods: {
    ok: function() {
      // Copy to avoid sending all vue getters/setters
      let action = { ...this.tmpAction }
      this.$emit('update', action)
    },
    hidden: function() {
      this.lastEditedArgument = null
    },
    getSubmodalId(suffix) {
      return this.modalId + '-' + suffix
    },
    updateArgument(argumentId, argument) {
      this.lastEditedArgument = argumentId
      this.tmpAction[argumentId] = argument
    },
    updateLastEditedArgument(argumentId) {
      this.lastEditedArgument = argumentId
    },
  },
  created() {
    this.tmpAction = { ...this.action }
  },
  props: {
    modalId: String,
    action: Object,
  }
}
</script>
