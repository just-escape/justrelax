<template>
  <div class="d-flex flex-column min-width-100px">
    <div class="d-flex justify-content-between">
      <div class="text-one-line-ellipsis mb-1">
        <CollapseChevron size="md" class="align-self-center" v-b-toggle="'collapse-register'"/>
        {{ row.name }} ({{ nActiveNodes }}/{{ nRegisteredNodes }})
      </div>
      <div class="pr-2">
        <i v-if="nActiveNodes == nRegisteredNodes" class="fa fa-fw fa-check text-jaffa"></i>
        <i v-else class="fa fa-fw fa-times text-danger"></i>
      </div>
    </div>
    <b-collapse id="collapse-register" :visible="false">
      <div v-for="node in row.widget_params.nodes" :key="node.name" class="d-flex flex-row justify-content-between align-items-center rows-striped px-2">
        <div>{{ node.name }}</div>
        <i v-if="new Date(nodeRegister[node.name]) - recentDt > 0" class="fa fa-fw fa-check text-jaffa"></i>
        <i v-else class="fa fa-fw fa-times text-danger"></i>
      </div>
    </b-collapse>
  </div>
</template>

<script>
import CollapseChevron from "@/components/common/CollapseChevron.vue"
import roomStore from "@/store/roomStore.js"

export default {
  name: "WidgetNodeRegister",
  components: {
    CollapseChevron,
  },
  data() {
    return {
      recentDt: new Date(),
    }
  },
  computed: {
    nodeRegister() {
      return roomStore.state.sessionData[this.roomId]["node_register"] || {}
    },
    nRegisteredNodes() {
      return this.row.widget_params.nodes.length
    },
    nActiveNodes() {
      let counter = 0
      for (let n of this.row.widget_params.nodes) {
        if (new Date(this.nodeRegister[n.name]) - this.recentDt > 0) {
          counter++
        }
      }
      return counter
    }
  },
  methods: {
    updatePingTable() {
      setTimeout(this.updatePingTable, 5000)
      let now = new Date()
      this.recentDt = new Date(now.getTime() - 10 * 1000)
    }
  },
  mounted() {
    this.updatePingTable()
  },
  props: [
    "defaultChannel",
    "row",
    "roomId",
  ]
}
</script>

<style scoped>
.rows-striped:nth-child(odd) {
  background: #4d4d4f;
}
</style>