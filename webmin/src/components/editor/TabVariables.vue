<template>
  <div class="container-fluid">
    <div v-for="v in variables" :key="v.name" class="row">
      {{ v.id }} - {{ v.name }} - {{ v.init_value }} - {{ v.list }} - {{ v.types }}
    </div>
    <textarea v-model="jsonVariables" cols="100" rows="20"></textarea>
  </div>
</template>

<script>
import editorStore from '@/store/editorStore.js'

export default {
  name: "TabVariables",
  computed: {
    variables() {
      return editorStore.state.variables
    },
    jsonVariables: {
      get() {
        return JSON.stringify(this.variables)
      },
      set(value) {
        editorStore.commit('setVariables', JSON.parse(value))
      },
    }
  }
}
</script>
