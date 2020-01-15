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
import valueModalMixin from '@/components/editor/valueModalMixin.js'

export default {
  name: "ValueModalList",
  mixins: [valueModalMixin],
  computed: {
    list: {
      get() {
        return JSON.stringify(this.valueBuffer.list)
      },
      set(value) {
        this.valueBuffer = {
          list: JSON.parse(value),
        }
        this.pushMyValue()
      },
    }
  },
  created() {
    if (typeof this.parentValue === "object" && this.parentValue.list !== undefined) {
      this.valueBuffer = this.parentValue
      this.pushMyValue()
    } else {
      this.valueBuffer = {list: []}
    }
  },
}
</script>
