<template>
  <div>
    <ContextLinksLine
      v-b-modal="modalId"
      class="pointer"
      :contextLinks="contextLinks"
    />

    <ContextModal
      @update="updateContent"
      :modalId="modalId"
      :contextType="contextType"
      :content="content"
    />
  </div>
</template>

<script>
import ContextLinksLine from '@/components/editor/ContextLinksLine.vue'
import ContextModal from '@/components/editor/ContextModal.vue'
import rulesStore from '@/store/rulesStore.js'

export default {
  name: "ContextLine",
  components: {
    ContextLinksLine,
    ContextModal,
  },
  computed: {
    modalId: function() {
      return this.contextType + '-' + this.content.index
    },
    contextLinks: function() {
      var contextLinks = [...rulesStore.state.contextTypes[this.contextType][this.content.type].contextLinks]
      for (var i = 0 ; i < contextLinks.length ; i++) {
        if (contextLinks[i].type === "argument") {
          contextLinks[i].argument = this.content[contextLinks[i].argumentId]
        }
      }
      return contextLinks
    },
  },
  methods: {
    updateContent: function(content) {
      content.index = this.content.index
      this.$emit('updateContent', content)
    },
  },
  props: {
    content: Object,
    contextType: String,
  }
}
</script>
