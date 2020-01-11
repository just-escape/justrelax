<template>
  <div>
    <div class="text-jaffa">
      <i class="fas fa-question fa-fw"></i> Conditions
    </div>
    <div class="container-fluid">
      <div class="row">
        <div class="col">
          <div class="d-flex flex-column">
            <ConditionLine
              v-for="c in conditions"
              :key="c.index"
              :condition="c"
              @updateCondition="updateCondition"
            />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import ConditionLine from "@/components/editor/ConditionLine.vue"

export default {
  name: 'TabRulesConditions',
  components: {
    ConditionLine,
  },
  methods: {
    updateCondition(condition) {
      this.$emit('updateCondition', condition)
    }
  },
  props: {
    conditions: Array,
  }
}
</script>
