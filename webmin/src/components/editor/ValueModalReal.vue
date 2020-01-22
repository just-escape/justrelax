<template>
  <div class="row mb-3">
    <div @click="pushMyValue" class="d-flex align-items-center col-3">
      <input type="radio" :checked="checked">
      <span class="ml-2">Real :</span>
    </div>
    <div class="col-9">
      <input
        placeholder="1.50"
        type="number"
        step="0.01"
        @focus="pushMyValue"
        @input="pushMyValue"
        v-model="valueBuffer"
      >
    </div>
  </div>
</template>

<script>
import valueModalMixin from '@/components/editor/valueModalMixin.js'

export default {
  name: "ValueModalReal",
  mixins: [valueModalMixin],
  methods: {
    pushMyValue() {
      this.$emit('pushValue', Number(this.valueBuffer))
    }
  },
  created() {
    if (
      Number(this.parentValue) === this.parentValue &&
      this.parentValue % 1 !== 0
    ) {
      this.valueBuffer = this.parentValue
      this.pushMyValue()
    } else {
      this.valueBuffer = 1.50
    }
  },
}
</script>
