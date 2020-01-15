<template>
  <div>
    <Template
      v-b-modal="modalId"
      class="pointer"
      :args="args"
      :links="links"
    />

    <ComponentModal
      @update="update"
      :modalId="modalId"
      :context="context"
      :component="component"
    />
  </div>
</template>

<script>
import Template from '@/components/editor/Template.vue'
import ComponentModal from '@/components/editor/ComponentModal.vue'
import editorStore from '@/store/editorStore.js'

export default {
  name: "ComponentInline",
  components: {
    Template,
    ComponentModal,
  },
  computed: {
    links: function() {
      return editorStore.state.templates[this.context][this.component.template].links
    },
    args: function() {
      return this.component.arguments
    },
  },
  methods: {
    update: function(component) {
      this.$emit('updateComponent', component)
    },
  },
  props: {
    component: Object,
    context: String,
    modalId: String,
  }
}
</script>
