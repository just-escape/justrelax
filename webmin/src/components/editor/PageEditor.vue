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
import rulesStore from '@/store/rulesStore.js'

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
    }
  },
  watch: {
    room: function(newValue) {
      var rules = newValue.rules
      rules = [
        {
          name: "press_button",
          index: 0,
          triggers: [
            {
              id: 1,
              index: 0,
              type: "incoming_message",
            }
          ],
          conditions: [
            {
              id: 3,
              index: 0,
              name: "condition 1",
            },
          ],
          actions: [
            {
              id: 1,
              index: 0,
              name: "switch_yellow_led_on",
            },
            {
              id: 2,
              index: 1,
              name: "cancel_red_and_green_led_hint_alarm"
            },
          ]
        },
        {
          name: "press_button2",
          index: 1,
          triggers: [
            {
              id: 1,
              index: 0,
              type: "incoming_message2",
            }
          ],
          conditions: [
            {
              id: 3,
              index: 0,
              name: "condition 2",
            },
          ],
          actions: [
            {
              id: 1,
              index: 0,
              name: "switch_yellow_led_on2",
            },
            {
              id: 2,
              index: 1,
              name: "cancel_red_and_green_led_hint_alarm2"
            },
          ]
        }
      ]
      rulesStore.commit('loadRules', rules)
      this.rules = JSON.stringify(rules)
    }
  },
  props: ['roomId']
}
</script>

<style src="vue-multiselect/dist/vue-multiselect.min.css"></style>
