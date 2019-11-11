<template>
  <MultiSelect
    v-model="selectedActions"
    :options="availableActions"
    :multiple="true"
    :close-on-select="false"
    :clear-on-select="false"
    :preserve-search="true"
    :taggable="true"
    placeholder="Select actions"
  ></MultiSelect>
</template>

<script>
import MultiSelect from 'vue-multiselect'
import rulesStore from '@/store/rulesStore.js'

export default {
  name: 'ActionSelector',
  components: {
    MultiSelect,
  },
  data() {
    return {
      selectedActions: []
    }
  },
  computed: {
    availableActions: function() {
      return Object.keys(rulesStore.state.actions)
    }
  },
  created() {
    this.selectedActions = this.initialActions
  },
  props: ['initialActions']
}
</script>
