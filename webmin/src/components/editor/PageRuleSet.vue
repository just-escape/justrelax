<template>
  <AppContent>
    <AppContentTitle class="d-flex flex-row" slot="header-left">
      <AppContentTitle class="mr-5">
        {{ ruleSet ? ruleSet.name + ' rule set' : 'Rule set not  found' }}
      </AppContentTitle>
      <b-button-group class="my-auto">
        <ButtonJaffa @click="save()">
          <i class="far fa-save fa-lg"></i>
        </ButtonJaffa>
      </b-button-group>
    </AppContentTitle>
    <div slot="main" v-if="!ruleSet">
      Rule set not found
    </div>
    <div slot="main" class="mt-2 h-100" v-else>
      <Rules/>
    </div>
  </AppContent>
</template>

<script>
import ButtonJaffa from '@/components/common/ButtonJaffa.vue'
import AppContent from '@/components/common/AppContent.vue'
import AppContentTitle from '@/components/common/AppContentTitle.vue'
import Rules from '@/components/editor/Rules.vue'
import roomStore from '@/store/roomStore.js'
import editorStore from '@/store/editorStore.js'

export default {
  name: 'PageRuleSet',
  components: {
    ButtonJaffa,
    AppContent,
    AppContentTitle,
    Rules,
  },
  computed: {
    ruleSet() {
      for (var ruleSet of roomStore.state.ruleSets) {
        if (ruleSet.id == this.ruleSetId) {
          return ruleSet
        }
      }

      return null
    },
  },
  methods: {
    save() {
      editorStore.dispatch('save', this.ruleSetId)
    },
  },
  created() {
    editorStore.dispatch('loadEditorData', this.ruleSetId)
  },
  props: ['ruleSetId'],
}
</script>
