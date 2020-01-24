<template>
  <div class="row mb-3">
    <div @click="pushMyValue" class="d-flex align-items-center col-3">
      <input type="radio" :checked="checked">
      <span class="ml-2">Object:</span>
    </div>
    <div class="col-9">
      <input
        placeholder="{key: value, key: value, ...}"
        class="w-100"
        @focus="pushMyValue"
        @input="pushMyValue"
        v-model="object"
      />
    </div>
  </div>
</template>

<script>
import valueModalMixin from '@/components/editor/valueModalMixin.js'

export default {
  name: "ValueModalObject",
  mixins: [valueModalMixin],
  computed: {
    object: {
      get() {
        return JSON.stringify(this.valueBuffer.object)
      },
      set(value) {
        this.valueBuffer = {
          object: JSON.parse(value),
        }
        this.pushMyValue()
      },
    }
  },
  created() {
    if (typeof this.parentValue === "object" && this.parentValue.object !== undefined) {
      this.valueBuffer = this.parentValue
      this.pushMyValue()
    } else {
      this.valueBuffer = {object: {}}
    }
  },
}
</script>
