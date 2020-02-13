<template>
  <div class="row mb-3">
    <div @click="pushMyValue" class="d-flex align-items-center col-3">
      <input type="radio" :checked="checked">
      <span class="ml-2">{{ $t('editor.integer') }}</span>
    </div>
    <div class="col-9">
      <input
        placeholder="1"
        type="number"
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
  name: "ValueModalInteger",
  mixins: [valueModalMixin],
  methods: {
    pushMyValue() {
      this.$emit('pushValue', Number(this.valueBuffer))
    }
  },
  created() {
    if (Number.isInteger(this.parentValue)) {
      this.valueBuffer = this.parentValue
      this.pushMyValue()
    } else {
      this.valueBuffer = 1
    }
  },
}
</script>
