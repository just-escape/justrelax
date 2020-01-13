<template>
  <b-modal
    :id="modalId"
    body-bg-variant="dark"
    body-text-variant="light"
    @ok="ok"
    @hidden="$emit('hidden')"
  >
    <div class="row mb-3">
      <div @click="setValueSource('variable')" class="d-flex align-items-center col-3">
        <input type="radio" value="variable" v-model="valueSource">
        <span class="ml-2">Variable :</span>
      </div>
      <div @focus="setValueSource('variable')" class="col-9">
        <select v-model="value.variable" @focus="setValueSource('variable')" class="w-100">
          <option
            v-for="(v, k) in variableValueOptions"
            :key="k"
            :value="k"
          >
            {{ v }}
          </option>
        </select>
      </div>
    </div>

    <div class="row mb-3">
      <div @click="setValueSource('function')" class="d-flex align-items-center col-3">
        <input type="radio" value="function" v-model="valueSource">
        <span class="ml-2">Function :</span>
      </div>
      <div @focus="setValueSource('function')" class="col-9">
        <select v-model="value.function" @focus="setValueSource('function')" class="w-100">
          <option
            v-for="(v, k) in functionValueOptions"
            :key="k"
            :value="k"
          >
            {{ v }}
          </option>
        </select>

        <div v-if="valueSource === 'function'">
          <span v-if="value.function === 'arithmetic'">
            <FormattedArgument
              class="mr-1"
              v-b-modal="getSubmodalId('left')"
              :argument="tmpLeft"
              :editable="true"
              :lastEdited="lastEditedArgument == 'tmpLeft'"
            />
            <select v-model="arithmeticOperatorValue" class="mr-1">
              <option v-for="(v, k) in arithmeticOperators" :key="k" :value="k">
                {{ v }}
              </option>
            </select>
            <FormattedArgument
              v-b-modal="getSubmodalId('right')"
              :argument="tmpRight"
              :editable="true"
              :lastEdited="lastEditedArgument == 'tmpRight'"
            />

            <ArgumentModal
              :modalId="getSubmodalId('left')"
              :argument="tmpLeft"
              @updateArgument="(argument) => tmpLeft = argument"
              @hidden="updateLastEditedArgument('tmpLeft')"
            />
            <ArgumentModal
              :modalId="getSubmodalId('right')"
              :argument="tmpRight"
              @updateArgument="(argument) => tmpRight = argument"
              @hidden="updateLastEditedArgument('tmpRight')"
            />
          </span>
          <span v-else-if="value.function === 'comparison'">
            <FormattedArgument
              class="mr-1"
              v-b-modal="getSubmodalId('left')"
              :argument="tmpLeft"
              :editable="true"
              :lastEdited="lastEditedArgument == 'tmpLeft'"
            />
            <select v-model="comparisonOperatorValue" class="mr-1">
              <option v-for="(v, k) in comparisonOperators" :key="k" :value="k">
                {{ v }}
              </option>
            </select>
            <FormattedArgument
              v-b-modal="getSubmodalId('right')"
              :argument="tmpRight"
              :editable="true"
              :lastEdited="lastEditedArgument == 'tmpRight'"
            />

            <ArgumentModal
              :modalId="getSubmodalId('left')"
              :argument="tmpLeft"
              @updateArgument="(argument) => tmpLeft = argument"
              @hidden="updateLastEditedArgument('tmpLeft')"
            />
            <ArgumentModal
              :modalId="getSubmodalId('right')"
              :argument="tmpRight"
              @updateArgument="(argument) => tmpRight = argument"
              @hidden="updateLastEditedArgument('tmpRight')"
            />
          </span>
          <span v-else-if="value.function === 'booleanLogic'">
            <FormattedArgument
              class="mr-1"
              v-b-modal="getSubmodalId('left')"
              :argument="tmpLeft"
              :editable="true"
              :lastEdited="lastEditedArgument == 'tmpLeft'"
            />
            <select v-model="booleanLogicOperatorValue" class="mr-1">
              <option v-for="(v, k) in booleanLogicOperators" :key="k" :value="k">
                {{ v }}
              </option>
            </select>
            <FormattedArgument
              v-b-modal="getSubmodalId('right')"
              :argument="tmpRight"
              :editable="true"
              :lastEdited="lastEditedArgument == 'tmpRight'"
            />

            <ArgumentModal
              :modalId="getSubmodalId('left')"
              :argument="tmpLeft"
              @updateArgument="(argument) => tmpLeft = argument"
              @hidden="updateLastEditedArgument('tmpLeft')"
            />
            <ArgumentModal
              :modalId="getSubmodalId('right')"
              :argument="tmpRight"
              @updateArgument="(argument) => tmpRight = argument"
              @hidden="updateLastEditedArgument('tmpRight')"
            />
          </span>
        </div>
      </div>
    </div>

    <div class="row mb-3">
      <div @click="setValueSource('object')" class="d-flex align-items-center col-3">
        <input type="radio" value="object" v-model="valueSource">
        <span class="ml-2">Object :</span>
      </div>
      <div class="col-9">
        TODO
      </div>
    </div>

    <div class="row mb-3">
      <div @click="setValueSource('list')" class="d-flex align-items-center col-3">
        <input type="radio" value="list" v-model="valueSource">
        <span class="ml-2">List :</span>
      </div>
      <div class="col-9">
        TODO
      </div>
    </div>

    <div class="row mb-3">
      <div @click="setValueSource('string')" class="d-flex align-items-center col-3">
        <input type="radio" value="string" v-model="valueSource">
        <span class="ml-2">String :</span>
      </div>
      <div class="col-9">
        <input
          placeholder="Any text"
          @focus="setValueSource('string')"
          class="w-100"
          v-model="value.string"
        >
      </div>
    </div>

    <div class="row mb-3">
      <div @click="setValueSource('integer')" class="d-flex align-items-center col-3">
        <input type="radio" value="integer" v-model="valueSource">
        <span class="ml-2">Integer :</span>
      </div>
      <div class="col-9">
        <input
          placeholder="1"
          type="number"
          @focus="setValueSource('integer')"
          v-model="value.integer"
        >
      </div>
    </div>

    <div class="row mb-3">
      <div @click="setValueSource('real')" class="d-flex align-items-center col-3">
        <input type="radio" value="real" v-model="valueSource">
        <span class="ml-2">Real :</span>
      </div>
      <div class="col-9">
        <input
          placeholder="1.50"
          type="number"
          step="0.01"
          @focus="setValueSource('real')"
          v-model="value.real"
        >
      </div>
    </div>

    <div class="row">
      <div @click="setValueSource('special')" class="d-flex align-items-center col-3">
        <input type="radio" value="special" v-model="valueSource">
        <span class="ml-2">Special :</span>
      </div>
      <div class="col-9">
        <select v-model="value.special" @focus="setValueSource('special')">
          <option
            v-for="(v, k) in specialValueOptions"
            :key="k"
            :value="k"
          >
            {{ v }}
          </option>
        </select>
      </div>
    </div>
  </b-modal>
</template>

<script>
import FormattedArgument from '@/components/editor/FormattedArgument.vue'
import rulesStore from '@/store/rulesStore.js'

export default {
  name: "ArgumentModal",
  components: {
    FormattedArgument,
  },
  data() {
    return {
      tmpArgument: undefined,
      valueSource: "string",
      value: {
        variable: "var1",
        function: "arithmetic",
        object: undefined,
        list: undefined,
        string: "hello",
        integer: 1,
        real: 1.50,
        special: "true",
      },
      variableValueOptions: {
        var1: "Variable 1",
        var2: "Variable 2",
        var3: "Variable 3",
      },
      functionValueOptions: {
        arithmetic: "Arithmetic",
        comparison: "Comparison",
        booleanLogic: "Boolean logic",
      },
      specialValueOptions: {
        true: "True",
        false: "False",
        none: "None",
      },
      arithmeticOperatorValue: "+",
      comparisonOperatorValue: "=",
      booleanLogicOperatorValue: "and",
      tmpLeft: 1,
      tmpRight: 2,
      lastEditedArgument: undefined,
    }
  },
  computed: {
    arithmeticOperators() {
      return rulesStore.state.functions.arithmetic.operators
    },
    comparisonOperators() {
      return rulesStore.state.functions.comparison.operators
    },
    booleanLogicOperators() {
      return rulesStore.state.functions.booleanLogic.operators
    },
  },
  methods: {
    ok: function() {
      let argument = undefined
      if (this.valueSource === "special") {
        if (this.value.special === "none") {
          argument = null
        } else if (this.value.special === "true") {
          argument = true
        } else if (this.value.special === "false") {
          argument = false
        }
      } else if (["string", "integer", "real"].includes(this.valueSource)) {
        argument = this.value[this.valueSource]
      } else if (this.valueSource === "list") {
        argument = []
      } else if (this.valueSource === "object") {
        argument = {}
      } else if (this.valueSource === "function") {
        if (this.value.function === "arithmetic") {
          argument = {
            left: this.tmpLeft,
            operator: this.arithmeticOperatorValue,
            right: this.tmpRight,
          }
        } else if (this.value.function === "comparison") {
          argument = {
            left: this.tmpLeft,
            operator: this.comparisonOperatorValue,
            right: this.tmpRight,
          }
        } else if (this.value.function === "booleanLogic") {
          argument = {
            left: this.tmpLeft,
            operator: this.booleanLogicOperatorValue,
            right: this.tmpRight,
          }
        }
      } else if (this.valueSource === "variable") {
        argument = this.value.variable
      }
      this.$emit('updateArgument', argument)
    },
    getSubmodalId(suffix) {
      return this.modalId + '-' + suffix
    },
    setValueSource: function(value) {
      this.valueSource = value
      this.lastEditedArgument = undefined
    },
    updateLastEditedArgument(argumentId) {
      this.lastEditedArgument = argumentId
    },
  },
  created() {
    if (this.argument === null) {
      this.valueSource = "special"
      this.value.special = "none"
    } else if (this.argument === true) {
      this.valueSource = "special"
      this.value.special = "true"
    } else if (this.argument === false) {
      this.valueSource = "special"
      this.value.special = "false"
    } else if (Number.isInteger(this.argument)) {
      this.valueSource = "integer"
      this.value.integer = this.argument
    } else if (Number(this.argument) === this.argument && this.argument % 1 !== 0) {
      this.valueSource = "float"
      this.value.float = this.argument
    } else if (typeof this.argument === "string") {
      this.valueSource = "string"
      this.value.string = this.argument
    } else if (typeof this.argument === "object") {
      if (this.argument.operator !== undefined) {
        if (Object.keys(this.arithmeticOperators).includes(this.argument.operator)) {
          this.valueSource = "function"
          this.value.function = "arithmetic"
          this.arithmeticOperatorValue = this.argument.operator
          this.tmpLeft = this.argument.left
          this.tmpRight = this.argument.right
        } else if (Object.keys(this.comparisonOperators).includes(this.argument.operator)) {
          this.valueSource = "function"
          this.value.function = "comparison"
          this.comparisonOperatorValue = this.argument.operator
          this.tmpLeft = this.argument.left
          this.tmpRight = this.argument.right
        } else if (Object.keys(this.booleanLogicOperators).includes(this.argument.operator)) {
          this.valueSource = "function"
          this.value.function = "booleanLogic"
          this.booleanLogicOperatorValue = this.argument.operator
          this.tmpLeft = this.argument.left
          this.tmpRight = this.argument.right
        }
      }
    }
  },
  props: ["modalId", "argument"],
}
</script>
