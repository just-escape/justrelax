<template>
  <div class="d-flex flex-row h-100">
    <div class="rules-list">
      <div class="d-flex flex-row mb-3">
        <h2 class="big-noodle size-15 align-self-center mb-0 mr-3">Subrules</h2>
        <b-button-group>
          <ButtonSmall class="position-relative">
            <i class="far fa-file fa-fw"></i>
            <i class="fas fa-plus bottom-right"></i>
          </ButtonSmall>
          <ButtonSmall class="position-relative">
            <i class="far fa-folder-open fa-fw"></i>
            <i class="fas fa-plus bottom-right"></i>
          </ButtonSmall>
        </b-button-group>
      </div>
      <div class="d-flex flex-column">
        <div v-for="r in rules" :key="r.index" class="pointer" @click="displayRule(r.index)">
          <i class="far fa-file fa-fw"></i> {{ r.name }}
        </div>
      </div>
    </div>
    <div class="container-fluid">
      <div class="row">
        <div class="col">
          <div class="d-flex flex-row mb-3">
            <div class="mr-3 align-self-center">Name of the rule</div>

            <b-button-group>
              <ButtonSmall class="position-relative" @click="addTrigger()">
                <i class="fas fa-exclamation fa-fw"></i>
                <i class="fas fa-plus bottom-right"></i>
              </ButtonSmall>
              <ButtonSmall class="position-relative" @click="addCondition()">
                <i class="fas fa-question fa-fw"></i>
                <i class="fas fa-plus bottom-right"></i>
              </ButtonSmall>
              <ButtonSmall class="position-relative" @click="addAction()">
                <i class="fas fa-play fa-fw"></i>
                <i class="fas fa-plus bottom-right"></i>
              </ButtonSmall>
            </b-button-group>
          </div>

          <div class="container-fluid">
            <div class="row mb-2">
              <div class="col">
                <TabRulesTriggers
                  :triggers="displayedRuleTriggers"
                  @updateTrigger="updateTrigger"
                />
              </div>
            </div>
            <div class="row mb-2">
              <div class="col">
                <TabRulesConditions
                  :conditions="displayedRuleConditions"
                  @updateCondition="updateCondition"
                />
              </div>
            </div>
            <div class="row">
              <div class="col">
                <TabRulesActions
                  :actions="displayedRuleActions"
                  @updateAction="updateAction"
                />
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import ButtonSmall from "@/components/common/ButtonSmall"
import TabRulesTriggers from "./TabRulesTriggers"
import TabRulesConditions from "./TabRulesConditions"
import TabRulesActions from "./TabRulesActions"
import rulesStore from "@/store/rulesStore.js"

export default {
  name: 'TabRules',
  components: {
    ButtonSmall,
    TabRulesTriggers,
    TabRulesConditions,
    TabRulesActions,
  },
  data() {
    return {
      displayRuleIndex: 0,
    }
  },
  computed: {
    rules: function() {
      return rulesStore.state.rules
    },
    displayedRule: function() {
      return rulesStore.state.rules[this.displayRuleIndex]
    },
    displayedRuleTriggers: function() {
      if (this.displayedRule === null) {
        return []
      } else {
        return this.displayedRule.triggers
      }
    },
    displayedRuleConditions: function() {
      if (this.displayedRule === null) {
        return []
      } else {
        return this.displayedRule.conditions
      }
    },
    displayedRuleActions: function() {
      if (this.displayedRule === null) {
        return []
      } else {
        return this.displayedRule.actions
      }
    },
  },
  methods: {
    displayRule: function(index) {
      this.displayRuleIndex = index
    },
    addTrigger: function() {
      rulesStore.commit('addTrigger', this.displayRuleIndex)
    },
    updateTrigger: function(trigger) {
      let ruleIndex = this.displayRuleIndex
      rulesStore.commit('updateTrigger', {ruleIndex, trigger})
    },
    addCondition: function() {
      rulesStore.commit('addCondition', this.displayRuleIndex)
    },
    updateCondition: function(condition) {
      let ruleIndex = this.displayRuleIndex
      rulesStore.commit('updateCondition', {ruleIndex, condition})
    },
    addAction: function() {
      rulesStore.commit('addAction', this.displayRuleIndex)
    },
    updateAction: function(action) {
      let ruleIndex = this.displayRuleIndex
      rulesStore.commit('updateAction', {ruleIndex, action})
    },
  }
}
</script>

<style scoped>
.rules-list {
  border-right: rgba(248, 249, 250, 0.2) 1px solid;
  padding-right: 15px;
  width: 200px;
}

.bottom-right {
  position: absolute;
  bottom: 0.2rem;
  right: 0.2rem;
  font-size: 70%;
}
</style>
