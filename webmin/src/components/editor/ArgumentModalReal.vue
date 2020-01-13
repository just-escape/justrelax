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
        v-model="contentBuffer"
      >
    </div>
  </div>
</template>

<script>
import argumentModalXMixin from '@/components/editor/argumentModalXMixin.js'

export default {
  name: "ArgumentModalReal",
  mixins: [argumentModalXMixin],
  created() {
    if (
      Number(this.parentArgument) === this.parentArgument &&
      this.parentArgument % 1 !== 0
    ) {
      this.contentBuffer = this.parentArgument
      this.pushMyValue()
    } else {
      this.contentBuffer = 1.50
    }
  },
}
</script>
