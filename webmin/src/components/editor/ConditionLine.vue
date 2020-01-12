<template>
  <div>
    <span v-b-modal="modalId" class="pointer">
      <span v-if="condition.type == 'condition 1'">
        Condition 1
      </span>
      <span v-else-if="condition.type == 'condition 2'">
        Condition 2
      </span>
      <span v-else-if="condition.type == 'condition 3'">
        Condition 3
      </span>
      <span v-else-if="condition.type == 'condition 4'">
        Condition 4
      </span>
      <span v-else-if="condition.name == 'condition 1'">
        Condition
      </span>
    </span>

    <ContextModal @update="updateCondition" :modalId="modalId" :contextType="'condition'" :content="condition"/>
  </div>
</template>

<script>
import ContextModal from '@/components/editor/ContextModal.vue'

export default {
  name: "ConditionLine",
  components: {
    ContextModal,
  },
  computed: {
    modalId: function() {
      return 'condition-' + this.condition.index
    }
  },
  methods: {
    updateCondition: function(condition) {
      condition.index = this.condition.index
      this.$emit('updateCondition', condition)
    }
  },
  props: {
    condition: Object,
  }
}
</script>
