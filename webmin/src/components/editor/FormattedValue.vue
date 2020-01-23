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
    <span>{{ format(value) }}</span>
  </span>
</template>

<script>
import editorStore from '@/store/editorStore.js'

export default {
  name: "FormattedValue",
  methods: {
    format(value) {
      // Null is not selectable on this interface
      if (value === null) {
        return "<Nothing>"
      } else if (value === true) {
        return "True"
      } else if (value === false) {
        return "False"
      } else if (typeof value === "number") {
        return value
      } else if (typeof value === "string") {
        if (value === "") {
          return "<Empty string>"
        } else {
          return value
        }
      } else if (typeof value === "object") {
        if (value.function !== undefined) {
          var formattedValue = ""
          let links = editorStore.state.templates.function[value.function].links
          for (var link of links) {
            if (link.type === 'text') {
              formattedValue += link.text
            } else if (link.type === 'argument') {
              formattedValue += this.format(value.arguments[link.key])
            }
          }
          return formattedValue
        } else if (value.variable !== undefined) {
          return value.variable
        } else if (value.object !== undefined) {
          var objectOutput = "{"
          let keys = Object.keys(value.object)
          for (var i = 0 ; i < keys.length ; i++) {
            objectOutput += this.format(keys[i]) + ": " + this.format(value.object[keys[i]])
            if (i !== keys.length - 1) {
              objectOutput += ", "
            }
          }
          objectOutput += "}"
          return objectOutput
        } else if (value.list !== undefined) {
          var listOutput = "["
          for (var j = 0 ; j < value.list.length ; j++) {
            listOutput += this.format(value.list[j])
            if (j !== value.list.length - 1) {
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
    value: {
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
