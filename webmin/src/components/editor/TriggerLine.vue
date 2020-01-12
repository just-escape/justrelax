<template>
  <div>
    <!-- <InlineSelect :options="options" :default="selected"/> -->
    <span v-b-modal="modalId" class="pointer">
      <span v-if="trigger.type == 'incoming_message'">
        A message has been received
      </span>
      <span v-else-if="trigger.type == 'timer_expired'">
        A timer has expired
      </span>
      <span v-else-if="trigger.type == 'session_ticked'">
        The session has ticked
      </span>
      <span v-else-if="trigger.type == 'session_started'">
        The game session has started
      </span>
      <span v-else-if="trigger.type == 'session_paused'">
        The session has paused
      </span>
      <span v-else-if="trigger.type == 'session_resumed'">
        The session has resumed
      </span>
    </span>

    <ContextModal @update="updateTrigger" :modalId="modalId" :contextType="'trigger'" :content="trigger"/>
  </div>
</template>

<script>
import ContextModal from '@/components/editor/ContextModal.vue'
// import InlineSelect from "@/components/common/InlineSelect.vue"

export default {
  name: "TriggerLine",
  components: {
    // InlineSelect,
    ContextModal,
  },
  computed: {
    modalId: function() {
      return 'trigger-' + this.trigger.index
    },
  },
  methods: {
    updateTrigger: function(trigger) {
      // Index might have been changed by something else
      trigger.index = this.trigger.index
      this.$emit('updateTrigger', trigger)
    }
  },
  props: {
    trigger: Object,
  }
}
</script>
