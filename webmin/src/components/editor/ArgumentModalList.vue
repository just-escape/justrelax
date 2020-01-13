<template>
  <div class="row mb-3">
    <div @click="pushMyValue" class="d-flex align-items-center col-3">
      <input type="radio" :checked="checked">
      <span class="ml-2">List :</span>
    </div>
    <div class="col-9">
      <input
        placeholder="[item, item, ...]"
        class="w-100"
        @focus="pushMyValue"
        @input="pushMyValue"
        v-model="list"
      />
    </div>
  </div>
</template>

<script>
import argumentModalXMixin from '@/components/editor/argumentModalXMixin.js'

export default {
  name: "ArgumentModalList",
  mixins: [argumentModalXMixin],
  computed: {
    list: {
      get() {
        return JSON.stringify(this.contentBuffer.list)
      },
      set(value) {
        this.contentBuffer = {
          list: JSON.parse(value),
        }
        this.pushMyValue()
      },
    }
  },
  created() {
    if (typeof this.parentArgument === "object" && this.parentArgument.list !== undefined) {
      this.contentBuffer = this.parentArgument
    } else {
      this.contentBuffer = {list: []}
    }
  },
}
</script>
