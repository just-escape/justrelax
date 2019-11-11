<template>
  <AppContent>
    <AppContentTitle slot="header-left">
      Editor
    </AppContentTitle>
    <div slot="main" v-if="!room">
      Room not found
    </div>
    <div slot="main" v-else>
      <b-tabs content-class="mt-3">
        <b-tab>
          <template v-slot:title>
            <i class="fas fa-list"></i> Rules
          </template>
          <PageEditorRules/>
        </b-tab>
        <b-tab>
          <template v-slot:title>
            <i class="fas fa-stopwatch"></i> Alarms
          </template>
          <PageEditorAlarms/>
        </b-tab>
        <b-tab>
          <template v-slot:title>
            <i class="fas fa-play"></i> Actions
          </template>
          <PageEditorActions/>
        </b-tab>
        <b-tab>
          <template v-slot:title>
            <i class="fas fa-question"></i> Conditions
          </template>
          <PageEditorConditions/>
        </b-tab>
        <b-tab>
          <template v-slot:title>
            <i class="far fa-handshake"></i> Hooks
          </template>
          <PageEditorHooks/>
        </b-tab>
        <b-tab>
          <template v-slot:title>
            <i class="fas fa-table"></i> Admin
          </template>
          <PageEditorAdmin/>
        </b-tab>
        <b-tab>
          <template v-slot:title>
            <i class="far fa-edit"></i> Text
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
import AppContent from '@/components/AppContent.vue'
import AppContentTitle from '@/components/AppContentTitle.vue'
import PageEditorActions from '@/components/PageEditorActions.vue'
import PageEditorAdmin from '@/components/PageEditorAdmin.vue'
import PageEditorAlarms from '@/components/PageEditorAlarms.vue'
import PageEditorConditions from '@/components/PageEditorConditions.vue'
import PageEditorHooks from '@/components/PageEditorHooks.vue'
import PageEditorRules from '@/components/PageEditorRules.vue'
import roomStore from '@/store/roomStore.js'
import rulesStore from '@/store/rulesStore.js'

export default {
  name: 'PageEditor',
  components: {
    AppContent,
    AppContentTitle,
    PageEditorActions,
    PageEditorAdmin,
    PageEditorAlarms,
    PageEditorConditions,
    PageEditorHooks,
    PageEditorRules,
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
    }
  },
  watch: {
    room: function(newValue) {
      var rules = newValue.rules
      rulesStore.commit('loadRules', rules)
      this.rules = JSON.stringify(rules)
    }
  },
  props: ['roomId']
}
</script>

<style src="vue-multiselect/dist/vue-multiselect.min.css"></style>
