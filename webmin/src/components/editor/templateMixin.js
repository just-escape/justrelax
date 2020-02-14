import editorStore from '@/store/editorStore.js'

export default {
  methods: {
    format(value) {
      // Null is not selectable on this interface
      if (value === null) {
        return this.$t("editor.nothing")
      } else if (value === true) {
        return "True"
      } else if (value === false) {
        return "False"
      } else if (typeof value === "number") {
        return value.toString()
      } else if (typeof value === "string") {
        if (value === "") {
          return this.$t("editor.empty_string")
        } else {
          return value
        }
      } else if (typeof value === "object") {
        if (value.function !== undefined) {
          var formattedValue = ""
          let links = editorStore.state.templates.function[value.function].links
          for (var link of links) {
            if (link.type === 'text') {
              formattedValue += this.$t('editor.links.' + value.function + '.' + link.locale)
            } else if (link.type === 'argument') {
              formattedValue += this.format(value.arguments[link.key])
            }
          }
          return "(" + formattedValue + ")"
        } else if (value.variable !== undefined) {
          if (value.variable === null) {
            return this.$t("editor.no_variable")
          } else {
            return value.variable
          }
        } /*else if (value.object !== undefined) {
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
        }*/
      }

      return this.$t("editor.error")
    }
  },
}
