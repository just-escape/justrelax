<template>
  <div class="row mb-3">
    <div @click="pushMyValueIfNotDisabled" class="d-flex align-items-center col-3">
      <input id="test" :disabled="disabled" type="radio" :checked="checked">
      <span :disabled="disabled" class="ml-2">{{ $t('editor.variable') }}</span>
    </div>
    <div class="col-9">
      <select v-model="selectedVariable" @focus="pushMyValueIfNotDisabled" :disabled="disabled" class="w-100">
        <option
          v-for="variable in variables"
          :key="variable.name"
          :value="variable.name"
        >
          {{ variable.name }}
        </option>
      </select>
    </div>
  </div>
</template>

<script>
import valueModalMixin from '@/components/editor/valueModalMixin.js'
import editorStore from '@/store/editorStore.js'

export default {
  name: "ValueModalVariable",
  mixins: [valueModalMixin],
  computed: {
    variables() {
      if (this.inputType === 'variable') {
        return editorStore.state.variables
      } else {
        let this_ = this
        let filtered_variables = editorStore.state.variables.filter(
          function(v) {
            return v.type === this_.inputType
          }
        )
        return filtered_variables
      }
    },
    disabled() {
      return this.variables.length === 0
    },
    selectedVariable: {
      get() {
        return this.valueBuffer.variable
      },
      set(value) {
        this.valueBuffer = {
          variable: value,
        }
        this.pushMyValue()
      }
    },
  },
  methods: {
    pushMyValueIfNotDisabled() {
      if (!this.disabled) {
        this.pushMyValue()
      }
    },
  },
  created() {
    if (typeof this.parentValue === "object" && this.parentValue.variable !== undefined) {
      this.valueBuffer = {variable: this.parentValue.variable}
      this.pushMyValue()
    } else {
      if (!this.disabled) {
        this.valueBuffer = {
          variable: this.variables[0].name
        }
      } else {
        this.valueBuffer = {
          variable: "",
        }
      }
    }
  },
  props: {
    inputType: String,
  },
}
</script>
