<template>
  <div class="row">
    <div @click="pushMyValue" class="d-flex align-items-center col-3">
      <input type="radio" :checked="checked">
      <span class="ml-2">Special :</span>
    </div>
    <div class="col-9">
      <select v-model="selectedContent" @focus="pushMyValue">
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
  name: "ValueModalSpecial",
  mixins: [valueModalMixin],
  data() {
    return {
      options: {
        true: "True",
        false: "False",
        none: "None",
      }
    }
  },
  computed: {
    selectedContent: {
      get() {
        if (this.valueBuffer === true) {
          return "true"
        } else if (this.valueBuffer === false) {
          return "false"
        } else if (this.valueBuffer === null) {
          return "none"
        } else {
          return undefined
        }
      },
      set(value) {
        if (value === "true") {
          this.valueBuffer = true
        } else if (value === "false") {
          this.valueBuffer = false
        } else if (value === "none") {
          this.valueBuffer = null
        }
        this.pushMyValue()
      }
    }
  },
  created() {
    if ([true, false, null].includes(this.parentValue)) {
      this.valueBuffer = this.parentValue
      this.pushMyValue()
    } else {
      this.valueBuffer = true
    }
  },
}
</script>
