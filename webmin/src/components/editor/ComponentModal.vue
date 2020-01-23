<template>
  <b-modal
    :id="modalId"
    body-bg-variant="dark"
    body-text-variant="light"
    @ok="ok"
    @show="show"
  >
    <select v-model="selectedTemplate" class="mr-2">
      <option
        v-for="t in orderedTemplates"
        :key="t.name"
        :value="t.name"
      >
        {{ t.name }}
      </option>
    </select>

    <TemplateEditable
      :args="args"
      :links="links"
      :modalId="modalId"
      @updateArgument="updateArgument"
    />
  </b-modal>
</template>

<script>
import TemplateEditable from '@/components/editor/TemplateEditable.vue'
import editorStore from '@/store/editorStore.js'

export default {
  name: "ComponentModal",
  components: {
    TemplateEditable,
  },
  data() {
    return {
      componentBuffer: {},
    }
  },
  computed: {
    templates() {
      return editorStore.state.templates[this.context]
    },
    orderedTemplates() {
      return editorStore.state.orderedTemplates[this.context]
    },
    links() {
      return this.templates[this.componentBuffer.template].links
    },
    args() {
      return this.componentBuffer.arguments
    },
    selectedTemplate: {
      get() {
        return this.componentBuffer.template
      },
      set(value) {
        this.componentBuffer.template = value

        var args = {}
        for (var link of this.templates[value].links) {
          if (link.type === "argument") {
            args[link.key] = link.default_value
          }
        }
        this.componentBuffer.arguments = args
      }
    },
  },
  methods: {
    ok: function() {
      this.$emit('update', JSON.parse(JSON.stringify(this.componentBuffer)))
    },
    updateArgument(key, value) {
      this.componentBuffer.arguments[key] = value
    },
    show: function() {
      this.reloadComponentBuffer()
    },
    reloadComponentBuffer: function() {
      this.componentBuffer = JSON.parse(JSON.stringify(this.component))
    },
  },
  created() {
    this.reloadComponentBuffer()
  },
  props: {
    modalId: String,
    context: String,
    component: Object,
  }
}
</script>
