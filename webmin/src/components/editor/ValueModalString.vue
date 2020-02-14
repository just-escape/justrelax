<template>
  <div class="row mb-3">
    <div @click="pushMyValue" class="d-flex align-items-center col-3">
      <input type="radio" :checked="checked">
      <span class="ml-2">{{ $t('editor.string') }}</span>
    </div>
    <div class="col-9">
      <input
        :placeholder="$t('editor.any_text')"
        class="w-100"
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
  name: "ValueModalString",
  mixins: [valueModalMixin],
  created() {
    if (typeof this.parentValue === "string") {
      this.valueBuffer = this.parentValue
      this.pushMyValue()
    } else if (this.parentValue === true) {
      // In case of empty string, the passed vue prop is :prop="''", which is equivalent to prop being true
      this.valueBuffer = ""
      this.pushMyValue()
    } else {
      this.valueBuffer = "hello"
    }
  },
}
</script>
