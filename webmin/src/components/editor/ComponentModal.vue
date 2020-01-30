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
            if (link.value_type === "variable") {
              // Determine the default value dynamically
              if (editorStore.state.variables.length > 0) {
                args[link.key] = {variable: editorStore.state.variables[0].name}
              } else {
                args[link.key] = {variable: null}
              }
            } else if (this.componentBuffer.template === 'set_variable' && link.key === 'value') {
              // Hardcoded behavior for special case
              let variable = this.getVariableFromName(args.variable_name.variable)
              link.value_type = variable === null ? "disabled" : variable.type
              args[link.key] = this.getDefaultValueFromValueType(link.value_type)
            } else {
              args[link.key] = JSON.parse(link.default_value)
            }
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

      // Hardcoded behavior for special case
      if (this.selectedTemplate === 'set_variable' && key === 'variable_name') {
        let variable = this.getVariableFromName(value.variable)
        for (var link of this.templates[this.selectedTemplate].links) {
          if (link.key === 'value' && link.value_type !== variable.type) {
            link.value_type = variable.type
            this.componentBuffer.arguments.value = this.getDefaultValueFromValueType(variable.type)
            return
          }
        }
      }
    },
    show: function() {
      this.reloadComponentBuffer()
    },
    reloadComponentBuffer: function() {
      this.componentBuffer = JSON.parse(JSON.stringify(this.component))
    },
    getVariableFromName: function(variableName) {
      for (var variable of editorStore.state.variables) {
        if (variable.name === variableName) {
          return variable
        }
      }
      return null
    },
    getDefaultValueFromValueType: function(valueType) {
      if (valueType === "string") {
        return "hello"
      } else if (valueType === "integer") {
        return 1
      } else if (valueType === "real") {
        return 1.5
      } else if (valueType === "boolean") {
        return true
      } else if (valueType === "object") {
        return {function: "last_created_object"}
      } else if (valueType === "disabled") {
        return null
      } else {
        // Bad value type (data is corrupted)
        return undefined
      }
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
