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
import argumentModalXMixin from '@/components/editor/argumentModalXMixin.js'

export default {
  name: "ArgumentModalSpecial",
  mixins: [argumentModalXMixin],
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
        if (this.contentBuffer === true) {
          return "true"
        } else if (this.contentBuffer === false) {
          return "false"
        } else if (this.contentBuffer === null) {
          return "none"
        } else {
          return undefined
        }
      },
      set(value) {
        if (value === "true") {
          this.contentBuffer = true
        } else if (value === "false") {
          this.contentBuffer = false
        } else if (value === "none") {
          this.contentBuffer = null
        }
        this.pushMyValue()
      }
    }
  },
  created() {
    if ([true, false, null].includes(this.parentArgument)) {
      this.contentBuffer = this.parentArgument
      this.pushMyValue()
    } else {
      this.contentBuffer = true
    }
  },
}
</script>
