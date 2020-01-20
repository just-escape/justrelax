<template>
  <div class="row">
    <div @click="pushMyValue" class="d-flex align-items-center col-3">
      <input type="radio" :checked="checked">
      <span class="ml-2">Boolean :</span>
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
  name: "ValueModalBoolean",
  mixins: [valueModalMixin],
  data() {
    return {
      options: {
        true: "True",
        false: "False",
      }
    }
  },
  computed: {
    selectedContent: {
      get() {
        if (this.valueBuffer === false) {
          return "false"
        } else {
          return "true"
        }
      },
      set(value) {
        if (value === "false") {
          this.valueBuffer = false
        } else {
          this.valueBuffer = true
        }
        this.pushMyValue()
      }
    }
  },
  created() {
    if ([true, false].includes(this.parentValue)) {
      this.valueBuffer = this.parentValue
      this.pushMyValue()
    } else {
      this.valueBuffer = true
    }
  },
}
</script>
