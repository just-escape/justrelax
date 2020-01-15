<template>
  <div class="row mb-3">
    <div @click="pushMyValue" class="d-flex align-items-center col-3">
      <input type="radio" :checked="checked">
      <span class="ml-2">Variable :</span>
    </div>
    <div class="col-9">
      <select v-model="selectedVariable" @focus="pushMyValue" class="w-100">
        <option
          v-for="(label, value) in options"
          :key="value"
          :value="value"
        >
          {{ label }}
        </option>
      </select>
    </div>
  </div>
</template>

<script>
import valueModalMixin from '@/components/editor/valueModalMixin.js'

export default {
  name: "ValueModalVariable",
  mixins: [valueModalMixin],
  data() {
    return {
      options: {
        var1: "Variable 1",
        var2: "Variable 2",
        var3: "Variable 3",
      },
    }
  },
  computed: {
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
  created() {
    if (typeof this.parentValue === "object" && this.parentValue.variable !== undefined) {
      this.valueBuffer = this.parentValue
      this.pushMyValue()
    } else {
      this.valueBuffer = {
        variable: Object.keys(this.options)[0]
      }
    }
  },
}
</script>
