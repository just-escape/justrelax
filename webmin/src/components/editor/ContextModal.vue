<template>
  <b-modal
    :id="modalId"
    body-bg-variant="dark"
    body-text-variant="light"
    @ok="ok"
  >
    <select v-model="selectedType" class="mr-2">
      <option
        v-for="ct in orderedContentTypes"
        :key="ct.name"
        :value="ct.name"
      >
        {{ ct.name }}
      </option>
    </select>

    <ContextLinksModal
      :args="args"
      :links="links"
      :modalId="modalId"
      @updateArgument="updateArgument"
    />
  </b-modal>
</template>

<script>
import ContextLinksModal from '@/components/editor/ContextLinksModal.vue'
import editorStore from '@/store/editorStore.js'

export default {
  name: "ActionModal",
  components: {
    ContextLinksModal,
  },
  data() {
    return {
      contextBuffer: {},
    }
  },
  computed: {
    contentTypes() {
      return editorStore.state.contextTypes[this.contextType]
    },
    orderedContentTypes() {
      return editorStore.state.orderedContextTypes[this.contextType]
    },
    links() {
      return this.contentTypes[this.contextBuffer.content_type].links
    },
    args() {
      return this.contextBuffer.arguments
    },
    selectedType: {
      get() {
        return this.contextBuffer.content_type
      },
      set(value) {
        this.contextBuffer.content_type = value

        var args = {}
        let links = this.contentTypes[value].links
        for (var i = 0 ; i < links.length ; i++) {
          if (links[i].link_type === "argument") {
            args[links[i].key] = links[i].default_value
          }
        }
        this.contextBuffer.arguments = args
      }
    },
  },
  methods: {
    ok: function() {
      this.$emit('update', JSON.parse(JSON.stringify(this.contextBuffer)))
    },
    updateArgument(argumentKey, argument) {
      this.contextBuffer.arguments[argumentKey] = argument
    },
  },
  created() {
    this.contextBuffer = JSON.parse(JSON.stringify(this.context))
  },
  props: {
    modalId: String,
    contextType: String,
    context: Object,
  }
}
</script>
