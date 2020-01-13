<template>
  <div class="row mb-3">
    <div @click="pushMyValue" class="d-flex align-items-center col-3">
      <input type="radio" :checked="checked">
      <span class="ml-2">Function :</span>
    </div>
    <div @focus="pushMyValue" class="col-9">
      <select v-model="selectedFunction" @focus="selectedFunction = '+'" class="w-100">
        <option
          v-for="(label, value) in options"
          :key="value"
          :value="value"
        >
          {{ label }}
        </option>
      </select>

      <ContextLinksModal
        :contextLinks="contextLinksBuffer"
        @updateArgument="updateArgument"
      />
    </div>
  </div>
</template>

<script>
import argumentModalXMixin from '@/components/editor/argumentModalXMixin.js'
import rulesStore from '@/store/rulesStore.js'

export default {
  name: "ArgumentModalFunction",
  mixins: [argumentModalXMixin],
  components: {
    ContextLinksModal: () => import('@/components/editor/ContextLinksModal.vue'),
  },
  data() {
    return {
      selectedFunction_: undefined,
      contextLinksBuffer: [],
    }
  },
  computed: {
    functionTypes() {
      return rulesStore.state.functionTypes
    },
    options() {
      var options = {}
      for (var i = 0 ; i < this.functionTypes.length ; i++) {
        options[this.functionTypes[i].name] = this.functionTypes[i].label
      }
      return options
    },
    selectedFunction: {
      get() {
        return this.selectedFunction_
      },
      set(value) {
        this.selectedFunction_ = value
        for (var i = 0 ; i < this.functionTypes.length ; i++) {
          if (this.functionTypes[i].name === this.selectedFunction) {
            this.contextLinksBuffer = JSON.parse(JSON.stringify(this.functionTypes[i].contextLinks))
            this.pushMyValue()
            return
          }
        }
      },
    }
  },
  methods: {
    pushMyValue() {
      var value = {
        operator: this.selectedFunction,
      }
      for (var i = 0 ; i < this.contextLinksBuffer.length ; i++) {
        if (this.contextLinksBuffer[i].type === "argument") {
          value[this.contextLinksBuffer[i].argumentId] = this.contextLinksBuffer[i].argument
        }
      }
      this.$emit('pushValue', value)
    },
    updateArgument(argumentId, argument) {
      for (var i = 0 ; i < this.contextLinksBuffer.length ; i++) {
        if (
          this.contextLinksBuffer[i].type === "argument" &&
          this.contextLinksBuffer[i].argumentId === argumentId
        ) {
          this.contextLinksBuffer[i].argument = argument
          this.pushMyValue()
          return
        }
      }
    },
    initArguments() {
      for (var i = 0 ; i < this.contextLinksBuffer.length ; i++) {
        if (this.contextLinksBuffer[i].type === "argument") {
          this.contextLinksBuffer[i].argument = this.parentArgument[this.contextLinksBuffer[i].argumentId]
        }
      }
    },
  },
  created() {
    if (typeof this.parentArgument === "object") {
      this.selectedFunction = this.parentArgument.operator
    }

    if (this.selectedFunction !== undefined) {
      this.initArguments()
      this.pushMyValue()
    } else {
      this.selectedFunction = "+"
    }
  }
}
</script>
