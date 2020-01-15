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

      <ContextLinksModal
        :modalId="modalId"
        :args="args"
        :links="links"
        @updateArgument="updateArgument"
      />
    </div>
  </div>
</template>

<script>
import argumentModalXMixin from '@/components/editor/argumentModalXMixin.js'
import editorStore from '@/store/editorStore.js'

export default {
  name: "ArgumentModalFunction",
  mixins: [argumentModalXMixin],
  components: {
    ContextLinksModal: () => import('@/components/editor/ContextLinksModal.vue'),
  },
  computed: {
    functions() {
      return editorStore.state.functions
    },
    orderedFunctions() {
      return editorStore.state.orderedFunctions
    },
    selectedFunction: {
      get() {
        return this.contentBuffer.operator
      },
      set(value) {
        this.contentBuffer.operator = value
        this.pushMyValue()
      },
    },
    links() {
      return this.functions[this.selectedFunction].links
    },
    args() {
      // The 'operator' key is unnecessarily passed but whatever
      return this.contentBuffer
    }
  },
  methods: {
    updateArgument(argumentKey, argument) {
      this.contentBuffer[argumentKey] = argument
      this.pushMyValue()
    },
  },
  created() {
    if (typeof this.parentArgument === "object" && this.parentArgument.operator !== undefined) {
      this.contentBuffer = JSON.parse(JSON.stringify(this.parentArgument))
      this.pushMyValue()
    } else {
      let default_function = this.orderedFunctions[0]

      this.contentBuffer = {
        operator: default_function.name,
      }

      // Init arguments from default values
      for (var i = 0 ; i < default_function.links.length ; i++) {
        if (default_function.links[i].link_type === "argument") {
          this.contentBuffer[default_function.links[i].key] = default_function.links[i].default_value
        }
      }
    }
  },
  props: {
    modalId: String,
  }
}
</script>
