<template>
  <div>
    <ContextLinksLine
      v-b-modal="modalId"
      class="pointer"
      :args="args"
      :links="links"
    />

    <ContextModal
      @update="updateContext"
      :modalId="modalId"
      :contextType="contextType"
      :context="context"
    />
  </div>
</template>

<script>
import ContextLinksLine from '@/components/editor/ContextLinksLine.vue'
import ContextModal from '@/components/editor/ContextModal.vue'
import editorStore from '@/store/editorStore.js'

export default {
  name: "ContextLine",
  components: {
    ContextLinksLine,
    ContextModal,
  },
  computed: {
    modalId: function() {
      return this.contextType + '-' + this.contextId
    },
    links: function() {
      return editorStore.state.contextTypes[this.contextType][this.context.content_type].links
    },
    args: function() {
      return this.context.arguments
    },
  },
  methods: {
    updateContext: function(context) {
      this.$emit('updateContext', context)
    },
  },
  props: {
    context: Object,
    contextId: Number,
    contextType: String,
  }
}
</script>
