<template>
  <span
    :class="{
      pointer: editable,
      'text-jaffa': editable,
      'text-underline': editable,
      'text-double': lastEdited,
      'font-italic': !editable,
    }"
  >
    <span>{{ formatArgument(argument) }}</span>
  </span>
</template>

<script>
import rulesStore from '@/store/rulesStore.js'

export default {
  name: "Argument",
  methods: {
    formatArgument(argument) {
      if (argument === null) {
        return "None"
      } else if (argument === true) {
        return "True"
      } else if (argument === false) {
        return "False"
      } else if (["string", "number"].includes(typeof argument)) {
        return argument
      } else if (typeof argument === "object") {
        if (argument.operator !== undefined) {
          if (Object.keys(rulesStore.state.functions.arithmetic.operators).includes(argument.operator)) {
            return '(' + this.formatArgument(argument.left) + ' ' + rulesStore.state.functions.arithmetic.operators[argument.operator] + ' ' + this.formatArgument(argument.right) + ')'
          } else if (Object.keys(rulesStore.state.functions.comparison.operators).includes(argument.operator)) {
            return '(' + this.formatArgument(argument.left) + ' ' + rulesStore.state.functions.comparison.operators[argument.operator] + ' ' + this.formatArgument(argument.right) + ')'
          } else if (Object.keys(rulesStore.state.functions.booleanLogic.operators).includes(argument.operator)) {
            return '(' + this.formatArgument(argument.left) + ' ' + rulesStore.state.functions.booleanLogic.operators[argument.operator] + ' ' + this.formatArgument(argument.right) + ')'
          }
        }
      }

      return "Undefined"
    }
  },
  props: {
    argument: {
      type: [Object, Boolean, String, Number],
      default: null,
    },
    editable: {
      type: Boolean,
      default: false,
    },
    lastEdited: {
      type: Boolean,
      default: false,
    }
  },
}
</script>

<style scoped>
.text-double {
  text-decoration-style: double;
}
</style>