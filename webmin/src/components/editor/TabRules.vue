<template>
  <div class="d-flex flex-row h-100">
    <div class="rules-list">
      <div class="d-flex flex-row mb-3">
        <h2 class="big-noodle size-15 align-self-center mb-0 mr-3">Rules</h2>
        <b-button-group>
          <ButtonSmall class="position-relative" @click="addRule()">
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
        <div v-if="displayedRule === null" class="col">
          Loading...
        </div>
        <div v-else class="col">
          <div class="d-flex flex-row mb-3">
            <div class="mr-3 align-self-center">{{ displayedRule.name }}</div>

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
                <ContextParagraph
                  :title="'Triggers'"
                  :contextType="'trigger'"
                  :lines="displayedRule.triggers"
                  @updateLine="updateTrigger"
                />
              </div>
            </div>
            <div class="row mb-2">
              <div class="col">
                <ContextParagraph
                  :title="'Conditions'"
                  :contextType="'condition'"
                  :lines="displayedRule.conditions"
                  @updateLine="updateCondition"
                />
              </div>
            </div>
            <div class="row">
              <div class="col">
                <ContextParagraph
                  :title="'Actions'"
                  :contextType="'action'"
                  :lines="displayedRule.actions"
                  @updateLine="updateAction"
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
import ContextParagraph from "@/components/editor/ContextParagraph.vue"
import editorStore from "@/store/editorStore.js"

export default {
  name: 'TabRules',
  components: {
    ButtonSmall,
    ContextParagraph,
  },
  data() {
    return {
      displayRuleIndex: 0,
    }
  },
  computed: {
    rules: function() {
      return editorStore.state.rules
    },
    displayedRule: function() {
      if (editorStore.state.rules[this.displayRuleIndex] === undefined) {
        return null
      } else {
        return editorStore.state.rules[this.displayRuleIndex]
      }
    },
  },
  methods: {
    displayRule: function(index) {
      this.displayRuleIndex = index
    },
    addRule: function() {
      editorStore.commit('addRule')
    },
    addTrigger: function() {
      editorStore.commit('addTrigger', this.displayRuleIndex)
    },
    updateTrigger: function(triggerIndex, trigger) {
      let ruleIndex = this.displayRuleIndex
      editorStore.commit('updateTrigger', {ruleIndex, triggerIndex, trigger})
    },
    addCondition: function() {
      editorStore.commit('addCondition', this.displayRuleIndex)
    },
    updateCondition: function(conditionIndex, condition) {
      let ruleIndex = this.displayRuleIndex
      editorStore.commit('updateCondition', {ruleIndex, conditionIndex, condition})
    },
    addAction: function() {
      editorStore.commit('addAction', this.displayRuleIndex)
    },
    updateAction: function(actionIndex, action) {
      let ruleIndex = this.displayRuleIndex
      editorStore.commit('updateAction', {ruleIndex, actionIndex, action})
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
