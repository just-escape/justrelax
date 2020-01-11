<template>
  <b-modal
    :id="modalId"
    @ok="ok"
  >
    <select v-model="selected" class="mr-2">
      <option disabled value="">Choose</option>
      <option v-for="(value, key) in options" :key="key" :value="key">{{ value }}</option>
    </select>
  </b-modal>
</template>

<script>
export default {
  name: "ActionModal",
  data() {
    return {
      tmpAction: undefined,
      options: {
        'switch_yellow_led_on': 'Action 1',
        'cancel_red_and_green_led_hint_alarm': 'Action 2',
        'action 3': 'Action 3',
        'action 4': 'Action 4',
      },
    }
  },
  computed: {
    selected: {
      get() {
        return this.tmpAction.name
      },
      set(value) {
        this.tmpAction.name = value
      }
    }
  },
  methods: {
    ok: function() {
      // Copy to avoid sending all vue getters/setters
      let action = { ...this.tmpAction }
      this.$emit('update', action)
    }
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
