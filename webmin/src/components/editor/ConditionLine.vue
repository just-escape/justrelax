<template>
  <div>
    <span v-b-modal="modalId" class="pointer">
      <span v-if="condition.name == 'condition 1'">
        Condition 1
      </span>
      <span v-else-if="condition.name == 'condition 2'">
        Condition 2
      </span>
      <span v-else-if="condition.name == 'condition 3'">
        Condition 3
      </span>
      <span v-else-if="condition.name == 'condition 4'">
        Condition 4
      </span>
    </span>

    <ConditionModal @update="updateCondition" :modalId="modalId" :condition="condition"/>
  </div>
</template>

<script>
import ConditionModal from '@/components/editor/ConditionModal.vue'

export default {
  name: "ConditionLine",
  components: {
    ConditionModal,
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
