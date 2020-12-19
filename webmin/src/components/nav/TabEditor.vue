<template>
  <div>
    <div class="d-flex flex-row justify-content-between p-3">
      <div>
        <i class="fas fa-tools fa-fw fa-lg mr-3"></i>Editor
      </div>
      <div class="d-flex flex-row">
        <CollapseChevron class="align-self-center" v-b-toggle="'collapse-editor'"/>
      </div>
    </div>
    <b-collapse id="collapse-editor" :visible="isVisible">
      <ul class="list-unstyled mb-0">
        <li v-for="ruleSet in ruleSets" :key="ruleSet.id" class="bgc-dark">
          <Tab :url="'/editor/' + ruleSet.id" icon="far fa-file-code fa-fw" :label="ruleSet.name"/>
        </li>
      </ul>
    </b-collapse>
  </div>
</template>

<script>
import Tab from '@/components/nav/Tab.vue'
import CollapseChevron from '@/components/common/CollapseChevron.vue'
import roomStore from '@/store/roomStore'

export default {
  name: 'TabEditor',
  components: {
    CollapseChevron,
    Tab,
  },
  computed: {
    ruleSets() {
      return roomStore.state.ruleSets
    },
    isVisible() {
      return this.$route.path.startsWith('/editor')
    },
  },
}
</script>

<style scoped>
ul > li {
  border-bottom: 1px solid #2e2e2e;
}

ul > li:last-child {
  border-bottom: 0;
}
</style>