<template>
  <div class="row mb-3">
    <div @click="pushMyValue" class="d-flex align-items-center col-3">
      <input type="radio" :checked="checked">
      <span class="ml-2">Integer :</span>
    </div>
    <div class="col-9">
      <input
        placeholder="1"
        type="number"
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
  name: "ArgumentModalInteger",
  mixins: [argumentModalXMixin],
  created() {
    if (Number.isInteger(this.parentArgument)) {
      this.contentBuffer = this.parentArgument
      this.pushMyValue()
    } else {
      this.contentBuffer = 1
    }
  },
}
</script>
