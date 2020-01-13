export default {
  data() {
    return {
      contentBuffer: undefined
    }
  },
  methods: {
    pushMyValue() {
      this.$emit('pushValue', this.contentBuffer)
    }
  },
  props: {
    parentArgument: [Object, Boolean, String, Number],
    checked: Boolean,
  }
}
