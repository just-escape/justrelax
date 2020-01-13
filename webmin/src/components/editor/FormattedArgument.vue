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
    <span>{{ format(argument) }}</span>
  </span>
</template>

<script>
export default {
  name: "FormattedArgument",
  methods: {
    format(argument) {
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
          var formattedArgument = argument.operator + ' ' + this.format(argument.right)
          if (argument.left !== undefined) {
            formattedArgument = this.format(argument.left) + ' ' + formattedArgument
          }
          return '(' + formattedArgument + ')'
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
