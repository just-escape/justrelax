<template>
  <div v-if="!disabled" class="row mb-3">
    <div @click="pushMyValue" class="d-flex align-items-center col-3">
      <input type="radio" :checked="checked">
      <span class="ml-2">{{ $t('editor.function') }}</span>
    </div>
    <div @focus="pushMyValue" class="col-9">
      <select v-model="selectedFunction" @focus="pushMyValue" class="w-100">
        <option
          v-for="f in selectableFunctions"
          :key="f.name"
          :value="f.name"
        >
          <span v-if="f.category">{{ $t('editor.categories.' + f.category) }} - </span>
          <span>{{ $t('editor.templates.' + f.name + ".name") }}</span>
        </option>
      </select>

      <TemplateEditable
        :modalId="modalId"
        :templateName="selectedFunction"
        :args="args"
        :links="links"
        @updateArgument="updateArgument"
      />
    </div>
  </div>
</template>

<script>
import valueModalMixin from '@/components/editor/valueModalMixin.js'
import editorStore from '@/store/editorStore.js'

export default {
  name: "ValueModalFunction",
  mixins: [valueModalMixin],
  components: {
    TemplateEditable: () => import('@/components/editor/TemplateEditable.vue'),
  },
  computed: {
    selectableFunctions() {
      return editorStore.state.templatesByContext[this.inputType]
    },
    disabled() {
      return this.selectableFunctions.length === 0
    },
    selectedFunction: {
      get() {
        return this.valueBuffer.template
      },
      set(value) {
        this.valueBuffer.template = value

        var args = {}
        for (var link of editorStore.state.templatesByName[value].links) {
          if (link.type === "argument") {
            args[link.key] = JSON.parse(link.default_value)
          }
        }
        this.valueBuffer.arguments = args
        this.pushMyValue()
      },
    },
    links() {
      return editorStore.state.templatesByName[this.selectedFunction].links
    },
    args() {
      return this.valueBuffer.arguments
    }
  },
  methods: {
    updateArgument(key, value) {
      this.$set(this.valueBuffer.arguments, key, value)
      this.pushMyValue()
    },
  },
  created() {
    if (typeof this.parentValue === "object" && this.parentValue.template !== undefined) {
      this.valueBuffer = JSON.parse(JSON.stringify(this.parentValue))
      this.pushMyValue()
    } else {
      if (!this.disabled) {
        let defaultFunction = this.selectableFunctions[0]

        this.$set(this, 'valueBuffer', {template: defaultFunction.name})

        this.$set(this.valueBuffer, 'arguments', {})
        for (var link of defaultFunction.links) {
          if (link.type === "argument") {
            this.valueBuffer.arguments[link.key] = JSON.parse(link.default_value)
          }
        }
      }
    }
  },
  props: {
    modalId: String,
    inputType: String,
  },
}
</script>
