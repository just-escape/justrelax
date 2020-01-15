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
        return "<Nothing>"
      } else if (argument === true) {
        return "True"
      } else if (argument === false) {
        return "False"
      } else if (typeof argument === "number") {
        return argument
      } else if (typeof argument === "string") {
        if (argument === "") {
          return "<Empty string>"
        } else {
          return argument
        }
      } else if (typeof argument === "object") {
        if (argument.operator !== undefined) {
          var formattedArgument = argument.operator + ' ' + this.format(argument.right)
          if (argument.left !== undefined) {
            formattedArgument = this.format(argument.left) + ' ' + formattedArgument
          }
          return '(' + formattedArgument + ')'
        } else if (argument.variable !== undefined) {
          return argument.variable
        } else if (argument.object !== undefined) {
          var objectOutput = "{"
          let keys = Object.keys(argument.object)
          for (var i = 0 ; i < keys.length ; i++) {
            objectOutput += this.format(keys[i]) + ": " + this.format(argument.object[keys[i]])
            if (i !== keys.length - 1) {
              objectOutput += ", "
            }
          }
          objectOutput += "}"
          return objectOutput
        } else if (argument.list !== undefined) {
          var listOutput = "["
          for (var j = 0 ; j < argument.list.length ; j++) {
            listOutput += this.format(argument.list[j])
            if (j !== argument.list.length - 1) {
              listOutput += ", "
            }
          }
          listOutput += "]"
          return listOutput
        }
      }

      return "<Error>"
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
