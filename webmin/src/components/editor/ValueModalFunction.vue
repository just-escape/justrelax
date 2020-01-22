<template>
  <div class="row mb-3">
    <div @click="pushMyValue" class="d-flex align-items-center col-3">
      <input type="radio" :checked="checked">
      <span class="ml-2">Function :</span>
    </div>
    <div @focus="pushMyValue" class="col-9">
      <select v-model="selectedFunction" @focus="pushMyValue" class="w-100">
        <option
          v-for="f in orderedFunctions"
          :key="f.name"
          :value="f.name"
        >
          {{ f.name }}
        </option>
      </select>

      <TemplateEditable
        :modalId="modalId"
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
    functions() {
      return editorStore.state.templates.function
    },
    orderedFunctions() {
      return editorStore.state.orderedTemplates.function
    },
    selectedFunction: {
      get() {
        return this.valueBuffer.function
      },
      set(value) {
        this.valueBuffer.function = value
        this.pushMyValue()
      },
    },
    links() {
      return this.functions[this.selectedFunction].links
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
    if (typeof this.parentValue === "object" && this.parentValue.function !== undefined) {
      this.valueBuffer = JSON.parse(JSON.stringify(this.parentValue))
      this.pushMyValue()
    } else {
      let defaultFunction = this.orderedFunctions[0]

      this.$set(this, 'valueBuffer', {function: defaultFunction.name})

      this.valueBuffer.arguments = {}
      for (var link of defaultFunction.links) {
        if (link.type === "argument") {
          this.valueBuffer.arguments[link.key] = link.default_value
        }
      }
    }
  },
  props: {
    modalId: String,
  }
}
</script>
