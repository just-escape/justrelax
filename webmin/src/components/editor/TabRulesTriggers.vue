<template>
  <div>
    <div class="text-jaffa">
      <i class="fas fa-exclamation fa-fw"></i> Triggers
    </div>
    <div class="container-fluid">
      <div class="row">
        <div class="col">
          <div class="d-flex flex-column">
            <Trigger v-for="t in triggers" :key="t.index" :trigger="t"/>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import Trigger from "@/components/editor/Trigger.vue"

export default {
  name: 'TabRulesTriggers',
  components: {
    Trigger,
  },
  props: {
    triggers: Array,
  }
}
</script>
