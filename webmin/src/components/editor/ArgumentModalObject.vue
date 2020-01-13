<template>
  <div class="row mb-3">
    <div @click="pushMyValue" class="d-flex align-items-center col-3">
      <input type="radio" :checked="checked">
      <span class="ml-2">Object :</span>
    </div>
    <div class="col-9">
      TODO
    </div>
  </div>
</template>

<script>
export default {
  name: "ArgumentModalObject",
  data() {
    return {
      contentBuffer: "obj"
    }
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
