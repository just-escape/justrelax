<template>
  <div>
    <div class="row">
      <div class="col">
        Name of the rule
        <div class="container-fluid">
          <div class="row">
            <div class="col">
              <TabRulesTriggers/>
            </div>
          </div>
          <div class="row">
            <div class="col">
              <TabRulesConditions/>
            </div>
          </div>
          <div class="row">
            <div class="col">
              <TabRulesActions/>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import TabRulesTriggers from "./TabRulesTriggers"
import TabRulesConditions from "./TabRulesConditions"
import TabRulesActions from "./TabRulesActions"

export default {
  name: 'TabRules',
  components: {
    TabRulesTriggers,
    TabRulesConditions,
    TabRulesActions,
  },
}
</script>
