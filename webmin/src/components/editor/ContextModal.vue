<template>
  <b-modal
    :id="modalId"
    body-bg-variant="dark"
    body-text-variant="light"
    @ok="ok"
  >
    <select v-model="contentType" class="mr-2">
      <option
        v-for="ct in Object.keys(contentTypes)"
        :key="contentTypes[ct].label"
        :value="ct"
      >
        {{ contentTypes[ct].label }}
      </option>
    </select>

    <ContextLinksModal
      :contextLinks="contentTypes[contentType].contextLinks"
      @updateArgument="updateArgument"
    />
  </b-modal>
</template>

<script>
import ContextLinksModal from '@/components/editor/ContextLinksModal.vue'
import rulesStore from '@/store/rulesStore.js'

export default {
  name: "ActionModal",
  components: {
    ContextLinksModal,
  },
  data() {
    return {
      contentType: undefined,
      contentTypes: {},
    }
  },
  methods: {
    ok: function() {
      let content = {
        type: this.contentType,
      }
      let currentContextLinks = this.contentTypes[this.contentType].contextLinks
      for (var i = 0 ; i < currentContextLinks.length ; i++) {
        if (currentContextLinks[i].type === "argument") {
          content[currentContextLinks[i].argumentId] = currentContextLinks[i].argument
        }
      }
      this.$emit('update', content)
    },
    updateArgument(argumentId, argument) {
      let currentContextLinks = this.contentTypes[this.contentType].contextLinks
      for (var i = 0 ; i < currentContextLinks.length ; i++) {
        if (currentContextLinks[i].type === "argument") {
          if (currentContextLinks[i].argumentId === argumentId) {
            currentContextLinks[i].argument = argument
            return
          }
        }
      }
    },
    initContent() {
      let currentContextLinks = this.contentTypes[this.contentType].contextLinks
      for (var i = 0 ; i < currentContextLinks.length ; i++) {
        if (currentContextLinks[i].type === "argument") {
          currentContextLinks[i].argumentId = this.content[currentContextLinks[i].argumentId]
        }
      }
    },
  },
  created() {
    this.$set(this, 'contentTypes', { ...rulesStore.state.contextTypes[this.contextType] })
    this.contentType = this.content.type
    if (this.contentType === undefined) {
      this.contentType = this.content.name
    }
    this.initContent()
  },
  props: {
    modalId: String,
    contextType: String,
    content: Object,
  }
}
</script>
