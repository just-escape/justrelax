<template>
  <div>
    <div class="text-jaffa">
      <i class="fas fa-question fa-fw"></i> Conditions
    </div>
    <div class="container-fluid">
      <div class="row">
        <div class="col">
          <div class="d-flex flex-column">
            <Condition v-for="c in conditions" :key="c.index" :condition="c"/>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import Condition from "@/components/editor/Condition.vue"

export default {
  name: 'TabRulesConditions',
  components: {
    Condition,
  },
  props: {
    conditions: Array,
  }
}
</script>
