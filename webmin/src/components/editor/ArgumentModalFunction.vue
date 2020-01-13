<template>
  <div class="row mb-3">
    <div @click="pushMyValue" class="d-flex align-items-center col-3">
      <input type="radio" :checked="checked">
      <span class="ml-2">Function :</span>
    </div>
    <div @focus="pushMyValue" class="col-9">
      <select v-model="selectedFunction" @focus="selectedFunction = 'arithmetic'" class="w-100">
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
      <!--<select v-model="arithmeticOperatorValue" class="mr-1">
        <option v-for="(v, k) in arithmeticOperators" :key="k" :value="k">
          {{ v }}
        </option>
      </select>-->
      <!--<select v-model="comparisonOperatorValue" class="mr-1">
        <option v-for="(v, k) in comparisonOperators" :key="k" :value="k">
          {{ v }}
        </option>
      </select>-->
      <!--<select v-model="booleanLogicOperatorValue" class="mr-1">
        <option v-for="(v, k) in booleanLogicOperators" :key="k" :value="k">
          {{ v }}
        </option>
      </select>-->
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
    arithmeticOperators() {
      return rulesStore.state.functions.arithmetic.operators
    },
    comparisonOperators() {
      return rulesStore.state.functions.comparison.operators
    },
    booleanLogicOperators() {
      return rulesStore.state.functions.booleanLogic.operators
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
      var value = {}
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
      if (Object.keys(this.arithmeticOperators).includes(this.parentArgument.operator)) {
        this.selectedFunction = "arithmetic"
      } else if (Object.keys(this.comparisonOperators).includes(this.parentArgument.operator)) {
        this.selectedFunction = "comparison"
      } else if (Object.keys(this.booleanLogicOperators).includes(this.parentArgument.operator)) {
        this.selectedFunction = "booleanLogic"
      }
    }

    if (this.selectedFunction !== undefined) {
      this.initArguments()
      this.pushMyValue()
    } else {
      this.selectedFunction = "arithmetic"
    }
  }
}
</script>
