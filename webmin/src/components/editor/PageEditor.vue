<template>
  <AppContent>
    <AppContentTitle slot="header-left">
      Editor
    </AppContentTitle>
    <div slot="main" v-if="!room">
      Room not found
    </div>
    <div slot="main" class="h-100" v-else>
      <b-tabs class="h-100" content-class="h-100 mt-3">
        <b-tab class="h-100">
          <template v-slot:title>
            <i class="fas fa-list fa-fw"></i> Rules
          </template>
          <TabRules/>
        </b-tab>
        <b-tab>
          <template v-slot:title>
            <i class="far fa-file-excel fa-fw"></i> Variables
          </template>
          <TabVariables/>
        </b-tab>
        <b-tab>
          <template v-slot:title>
            <i class="fas fa-table fa-fw"></i> Admin
          </template>
          <TabAdmin/>
        </b-tab>
        <b-tab>
          <template v-slot:title>
            <i class="far fa-edit fa-fw"></i> Text
          </template>

          <button class="btn-block" @click="updateRules">Save</button>
          <textarea
            style="background: #2e2e2e;"
            class="rounded"
            cols="100"
            rows="30"
            v-model="rules"
          ></textarea>
        </b-tab>
      </b-tabs>
    </div>
  </AppContent>
</template>

<script>
import AppContent from '@/components/common/AppContent.vue'
import AppContentTitle from '@/components/common/AppContentTitle.vue'
import TabRules from '@/components/editor/TabRules.vue'
import TabVariables from '@/components/editor/TabVariables.vue'
import TabAdmin from '@/components/editor/TabAdmin.vue'
import roomStore from '@/store/roomStore.js'
import editorStore from '@/store/editorStore.js'

export default {
  name: 'PageEditor',
  components: {
    AppContent,
    AppContentTitle,
    TabRules,
    TabVariables,
    TabAdmin,
  },
  data() {
    return {
      rules: '',
    }
  },
  computed: {
    room() {
      return roomStore.getters.room(this.roomId)
    },
  },
  methods: {
    updateRules() {
      var roomId = this.roomId
      var rules = this.rules
      roomStore.dispatch("updateRules", {roomId, rules})
    },
    loadEditorData() {
      editorStore.dispatch('loadTemplates')
      editorStore.dispatch('loadScenario')
    }
  },
  created() {
    this.loadEditorData()
  },
  props: ['roomId']
}
</script>

<style src="vue-multiselect/dist/vue-multiselect.min.css"></style>
