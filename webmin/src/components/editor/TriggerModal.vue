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
  name: "TriggerModal",
  data() {
    return {
      tmpTrigger: undefined,
      options: {
        incoming_message: 'Message received',
        timer_expired: 'Timer expired',
        session_ticked: 'Session tick',
        session_started: 'Session started',
        session_paused: 'Session paused',
        session_resumed: 'Session resumed',
      },
    }
  },
  computed: {
    selected: {
      get() {
        return this.tmpTrigger.type
      },
      set(value) {
        this.tmpTrigger.type = value
      }
    }
  },
  methods: {
    ok: function() {
      // Copy to avoid sending all vue getters/setters
      let trigger = { ...this.tmpTrigger }
      this.$emit('update', trigger)
    }
  },
  created() {
    this.tmpTrigger = { ...this.trigger }
  },
  props: {
    modalId: String,
    trigger: Object,
  }
}
</script>
