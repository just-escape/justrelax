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
        v-for="t in templates"
        :key="t.name"
        :value="t.name"
      >
        <span v-if="t.category">{{ $t('editor.categories.' + t.category) }} - </span>
        <span>{{ $t("editor.templates." + t.name + ".name") }}</span>
      </option>
    </select>

    <Template
      :args="args"
      :links="links"
      :modalId="modalId"
      :templateName="selectedTemplate"
      :editable="true"
      @updateArgument="updateArgument"
    />
  </b-modal>
</template>

<script>
import Template from '@/components/editor/Template.vue'
import editorStore from '@/store/editorStore.js'

export default {
  name: "ComponentModal",
  components: {
    Template,
  },
  data() {
    return {
      componentBuffer: {},
    }
  },
  computed: {
    component() {
      return editorStore.getters.dataFromFQDN(this.fqdn)
    },
    templates() {
      return editorStore.state.templatesByContext[this.context]
    },
    links() {
      return editorStore.state.templatesByName[this.componentBuffer.template].links
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
        for (var link of editorStore.state.templatesByName[value].links) {
          if (link.type === "argument") {
            if (link.value_type === "timer") {
              // Determine the default value dynamically
              let timerVariables = editorStore.state.variables.filter(v => v.type === "timer")
              if (timerVariables.length > 0) {
                args[link.key] = {variable: timerVariables[0].name}
              } else {
                args[link.key] = {variable: null}
              }
            } else if (link.value_type === "variable") {
              // Determine the default value dynamically
              if (editorStore.state.variables.length > 0) {
                args[link.key] = {variable: editorStore.state.variables[0].name}
              } else {
                args[link.key] = {variable: null}
              }
            } else if (this.componentBuffer.template === 'set_variable' && link.key === 'value') {
              // Hardcoded behavior for special case
              let variable = this.getVariableFromName(args.variable.variable)
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
      let fqdn = this.fqdn
      let data = JSON.parse(JSON.stringify(this.componentBuffer))
      editorStore.commit('setDataFromFQDN', {fqdn, data})
    },
    updateArgument(key, value) {
      this.$set(this.componentBuffer.arguments, key, value)

      // Hardcoded behavior for special case
      if (this.selectedTemplate === 'set_variable' && key === 'variable') {
        let variable = this.getVariableFromName(value.variable)
        for (var link of editorStore.state.templatesByName[this.selectedTemplate].links) {
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
        return {template: "last_created_object"}
      } else if (valueType === "timer") {
        return {template: "expiring_timer"}
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

    // Hardcoded behavior for special case
    if (this.componentBuffer.template === 'set_variable') {
      let variable = this.getVariableFromName(this.componentBuffer.arguments.variable.variable)
      if (variable !== null) {
        for (var link of editorStore.state.templatesByName.set_variable.links) {
          if (link.key === 'value') {
            link.value_type = variable.type
            return
          }
        }
      }
    }
  },
  props: {
    modalId: String,
    context: String,
    fqdn: Array,
  }
}
</script>
