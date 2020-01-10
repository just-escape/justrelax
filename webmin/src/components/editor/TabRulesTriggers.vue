<template>
  <div>
    <div class="text-jaffa">
      <i class="fas fa-exclamation fa-fw"></i> Triggers
    </div>
    <div class="container-fluid">
      <div class="row">
        <div class="col">
          <div class="d-flex flex-column">
            <TriggerLine
              v-for="t in triggers"
              :key="t.index"
              :trigger="t"
              @updateTrigger="updateTrigger"
            />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import TriggerLine from "@/components/editor/TriggerLine.vue"

export default {
  name: 'TabRulesTriggers',
  components: {
    TriggerLine,
  },
  methods: {
    updateTrigger(trigger) {
      this.$emit('updateTrigger', trigger)
    }
  },
  props: {
    triggers: Array,
  }
}
</script>
