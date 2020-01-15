export default {
  data() {
    return {
      valueBuffer: undefined
    }
  },
  methods: {
    pushMyValue() {
      this.$emit('pushValue', this.valueBuffer)
    }
  },
  props: {
    parentValue: [Object, Boolean, String, Number],
    checked: Boolean,
  }
}
