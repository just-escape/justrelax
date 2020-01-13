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
      let contentTypes = rulesStore.state.contextTypes[this.contextType]
      for (var i = 0 ; i < contentTypes.length ; i++) {
        if (contentTypes[i].name === this.content.type) {
          var contextLinks = JSON.parse(JSON.stringify(contentTypes[i].contextLinks))
          for (var j = 0 ; j < contextLinks.length ; j++) {
            if (contextLinks[j].type === "argument") {
              contextLinks[j].argument = this.content[contextLinks[j].argumentId]
            }
          }
          return contextLinks
        }
      }
      return [{type: "text", text: "error"}]
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
