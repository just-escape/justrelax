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
          <TabRules/>
        </b-tab>
        <b-tab>
          <template v-slot:title>
            <i class="fas fa-stopwatch"></i> Alarms
          </template>
          <TabAlarms/>
        </b-tab>
        <b-tab>
          <template v-slot:title>
            <i class="fas fa-play"></i> Actions
          </template>
          <TabActions/>
        </b-tab>
        <b-tab>
          <template v-slot:title>
            <i class="fas fa-question"></i> Conditions
          </template>
          <TabConditions/>
        </b-tab>
        <b-tab>
          <template v-slot:title>
            <i class="far fa-handshake"></i> Hooks
          </template>
          <TabHooks/>
        </b-tab>
        <b-tab>
          <template v-slot:title>
            <i class="fas fa-table"></i> Admin
          </template>
          <TabAdmin/>
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
import AppContent from '@/components/common/AppContent.vue'
import AppContentTitle from '@/components/common/AppContentTitle.vue'
import TabActions from '@/components/editor/TabActions.vue'
import TabAdmin from '@/components/editor/TabAdmin.vue'
import TabAlarms from '@/components/editor/TabAlarms.vue'
import TabConditions from '@/components/editor/TabConditions.vue'
import TabHooks from '@/components/editor/TabHooks.vue'
import TabRules from '@/components/editor/TabRules.vue'
import roomStore from '@/store/roomStore.js'
import rulesStore from '@/store/rulesStore.js'

export default {
  name: 'PageEditor',
  components: {
    AppContent,
    AppContentTitle,
    TabActions,
    TabAdmin,
    TabAlarms,
    TabConditions,
    TabHooks,
    TabRules,
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
