<template>
  <div class="row mb-3">
    <div @click="pushMyValue" class="d-flex align-items-center col-3">
      <input type="radio" :checked="checked">
      <span class="ml-2">String :</span>
    </div>
    <div class="col-9">
      <input
        placeholder="Any text"
        class="w-100"
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
  name: "ArgumentModalString",
  mixins: [argumentModalXMixin],
  created() {
    if (typeof this.parentArgument === "string") {
      this.contentBuffer = this.parentArgument
      this.pushMyValue()
    } else {
      this.contentBuffer = "hello"
    }
  },
}
</script>
