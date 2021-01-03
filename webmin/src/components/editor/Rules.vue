<template>
  <div class="d-flex flex-row h-100">
    <div class="rules-list">
      <div class="d-flex flex-row mb-3">
        <h2 class="big-noodle size-15 align-self-center mb-0 mr-3">{{ $t('editor.rules') }}</h2>
        <b-button-group>
          <ButtonSmall class="position-relative" @click="addRule()">
            <i class="far fa-file fa-fw"></i>
            <i class="fas fa-plus bottom-right"></i>
          </ButtonSmall>
        </b-button-group>
      </div>
      <div class="d-flex flex-column">
        <draggable
          @start="onDragStart"
          @update="onDragUpdate"
          @end="onDragUpdate"
          :list="rules"
          :group="{name: 'rules'}"
        >
          <div
            v-for="(r, index) in rules"
            :key="index"
            class="rounded"
            @click="ruleClicked(index)"
            :class="{'bgc-dark': displayedRuleIndex === index}"
          >
            <i class="mr-1 far fa-file fa-fw"></i>{{ r.name }}
          </div>
        </draggable>
      </div>
    </div>
    <div class="container-fluid">
      <div class="row">
        <div v-if="displayedRule === null" class="col">
          {{ $t('editor.loading') }}
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
                <ComponentParagraph
                  :root="true"
                  :title="$t('editor.triggers')"
                  context="trigger"
                  :fqdn="['rules', displayedRuleIndex, 'content', 'triggers']"
                />
              </div>
            </div>
            <div class="row mb-2">
              <div class="col">
                <ComponentParagraph
                  :root="true"
                  :title="$t('editor.conditions')"
                  context="condition"
                  :fqdn="['rules', displayedRuleIndex, 'content', 'conditions']"
                />
              </div>
            </div>
            <div class="row">
              <div class="col">
                <ComponentParagraph
                  :root="true"
                  :title="$t('editor.actions')"
                  context="action"
                  :fqdn="['rules', displayedRuleIndex, 'content', 'actions']"
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
import ComponentParagraph from "@/components/editor/ComponentParagraph.vue"
import editorStore from "@/store/editorStore.js"
import draggable from "vuedraggable"

export default {
  name: 'TabRules',
  components: {
    draggable,
    ButtonSmall,
    ComponentParagraph,
  },
  computed: {
    rules: {
      get() {
        return editorStore.state.rules
      },
      set(value) {
        let fqdn = ['rules']
        let data = value
        editorStore.commit('setDataFromFQDN', {fqdn, data})
      },
    },
    displayedRule: function() {
      return editorStore.getters.displayedRule
    },
    displayedRuleIndex: function() {
      return editorStore.state.displayedRuleIndex
    },
  },
  methods: {
    ruleClicked: function(index) {
      let fqdn = ['rules', index]
      editorStore.commit('setSelectedFQDN', fqdn)
    },
    addRule: function() {
      let fqdn = ['rules']
      let newRuleIndex = editorStore.state.rules.length + 1
      let data = {
        content: {
          triggers: [],
          conditions: [],
          actions: [],
        },
        name: "Rule " + newRuleIndex,
      }
      editorStore.commit('pushDataFromFQDN', {fqdn, data})

      if (newRuleIndex === 1) {
        editorStore.commit('setSelectedFQDN', ['rules', 0])
      }
    },
    addTrigger: function() {
      editorStore.dispatch('addComponent', 'trigger')
    },
    addCondition: function() {
      editorStore.dispatch('addComponent', 'condition')
    },
    addAction: function() {
      editorStore.dispatch('addComponent', 'action')
    },
    onDragStart: function(event) {
      var fqdn = ['rules', event.oldIndex]
      editorStore.commit('setSelectedFQDN', fqdn)
    },
    onDragUpdate: function(event) {
      var fqdn = ['rules', event.newIndex]
      editorStore.commit('setSelectedFQDN', fqdn)
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
