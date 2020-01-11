<template>
  <div>
    <span v-b-modal="modalId" class="pointer">
      <span v-if="action.name == 'switch_yellow_led_on'">
        Action 1.
      </span>
      <span v-else-if="action.name == 'cancel_red_and_green_led_hint_alarm'">
        Action 2.
      </span>
      <span v-else-if="action.name == 'action 3'">
        Action 3.
      </span>
      <span v-else-if="action.name == 'action 4'">
        Action 4.
      </span>
    </span>

    <ActionModal @update="updateAction" :modalId="modalId" :action="action"/>
  </div>
</template>

<script>
import ActionModal from '@/components/editor/ActionModal.vue'

export default {
  name: "ActionLine",
  components: {
    ActionModal,
  },
  computed: {
    modalId: function() {
      return 'action-' + this.action.index
    }
  },
  methods: {
    updateAction: function(action) {
      action.index = this.action.index
      this.$emit('updateAction', action)
    }
  },
  props: {
    action: Object,
  }
}
</script>
