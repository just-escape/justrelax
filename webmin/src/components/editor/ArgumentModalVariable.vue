<template>
  <div class="row mb-3">
    <div @click="pushMyValue" class="d-flex align-items-center col-3">
      <input type="radio" :checked="checked">
      <span class="ml-2">Variable :</span>
    </div>
    <div @focus="pushMyValue" class="col-9">
      <select v-model="value.variable" @focus="pushMyValue" class="w-100">
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
export default {
  name: "ArgumentModalVariable",
  data() {
    return {
      contentBuffer: "var1",
      options: {
        var1: "Variable 1",
        var2: "Variable 2",
        var3: "Variable 3",
      },
    }
  },
  computed: {
    selectedContent: {
      get() {
        return this.contentBuffer
      },
      set(value) {
        this.contentBuffer = value
        this.pushMyValue()
      }
    },
  },
  methods: {
    pushMyValue() {
      this.$emit('pushValue', this.contentBuffer)
    }
  },
  created() {
    // TODO
  },
  props: {
    parentArgument: [Object, Boolean, String, Number],
    checked: Boolean,
  }
}
</script>
