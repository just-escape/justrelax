<template>
  <b-modal
    :id="modalId"
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
          <option>Fonction 2</option>
        </select>
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
export default {
  name: "ArgumentModal",
  data() {
    return {
      tmpArgument: undefined,
      valueSource: "string",
      value: {
        variable: "var1",
        function: "f1",
        object: undefined,
        list: undefined,
        string: undefined,
        integer: undefined,
        real: undefined,
        special: "true",
      },
      variableValueOptions: {
        var1: "Variable 1",
        var2: "Variable 2",
        var3: "Variable 3",
      },
      functionValueOptions: {
        f1: "Function 1",
        f2: "Function 2",
        f3: "Function 3",
      },
      specialValueOptions: {
        true: "True",
        false: "False",
        none: "None",
      },
    }
  },
  methods: {
    ok: function() {
      let argument = undefined
      if (this.valueSource == "special") {
        if (this.value.special == "none") {
          argument = null
        } else if (this.value.special == "true") {
          argument = true
        } else if (this.value.special == "false") {
          argument = false
        }
      } else if (["string", "integer", "real"].includes(this.valueSource)) {
        argument = this.value[this.valueSource]
      } else if (this.valueSource == "list") {
        argument = []
      } else if (this.valueSource == "object") {
        argument = {}
      } else if (this.valueSource == "function") {
        argument = this.value.function
      } else if (this.valueSource == "variable") {
        argument = this.value.variable
      }
      this.$emit('updateArgument', argument)
    },
    setValueSource: function(value) {
      this.valueSource = value
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
    }
  },
  props: ["modalId", "argument"],
}
</script>
