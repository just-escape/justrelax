<template>
  <div @click="clicked">
    <i v-if="!editable" class="mr-1 fa-fw" :class="icon"></i>

    <span v-for="link in links" :key="link.key">
      <span v-if="link.type === 'text'">{{ $t('editor.templates.' + templateName + '.' + link.locale) }}</span>
      <span v-else-if="link.type === 'argument'">
        <FormattedValue
          v-b-modal="getModalId(link.key)"
          :formattedContent="format(args[link.key])"
          :editable="editable"
          :editDisabled="isEditDisabled(link)"
          :lastEdited="lastEditedArgumentKey === link.key"
        />
        <ValueModal
          v-if="!isEditDisabled(link) && editable"
          :modalId="getModalId(link.key)"
          :value="args[link.key]"
          :inputType="link.value_type"
          :templateName="templateName"
          :predefinedChoices="link.predefined_choices"
          @update="(value) => updateArgument(link.key, value)"
          @hidden="updateLastEditedArgument(link.key)"
        />
      </span>
    </span>
  </div>
</template>

<script>
import FormattedValue from '@/components/editor/FormattedValue.vue'
import ValueModal from '@/components/editor/ValueModal.vue'
import editorStore from '@/store/editorStore.js'

export default {
  name: "Template",
  components: {
    FormattedValue,
    ValueModal,
  },
  data() {
    return {
      lastEditedArgumentKey: undefined,
    }
  },
  computed: {
    icon() {
      return editorStore.getters.iconFromTemplate(this.templateName)
    },
    getModalId() {
      return (index) => {
        return this.modalId + '-' + index
      }
    },
  },
  methods: {
    updateArgument(key, value) {
      this.lastEditedArgumentKey = key
      this.$emit('updateArgument', key, value)
    },
    updateLastEditedArgument(argumentKey) {
      this.lastEditedArgumentKey = argumentKey
    },
    isEditDisabled(link) {
      // Dirty. This should be an info from the parent component.
      return link.value_type === 'disabled' || (link.value_type === 'variable' && editorStore.state.variables.length === 0)
    },
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
        if (value.template !== undefined) {
          var formattedValue = ""
          let links = editorStore.state.templatesByName[value.template].links
          for (var link of links) {
            if (link.type === 'text') {
              formattedValue += this.$t('editor.templates.' + value.template + '.' + link.locale)
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
        }
      }

      return this.$t("editor.error")
    },
    clicked() {
      this.$emit('click')
      if (!this.editable) {
        if (editorStore.state.selectedFQDN.toString() === this.fqdn.toString()) {
          this.$bvModal.show(this.modalId)
        } else {
          editorStore.commit('setSelectedFQDN', this.fqdn)
        }
      }
    }
  },
  watch: {
    templateName() {
      this.lastEditedArgumentKey = undefined
    },
    $i18n() {
      // Trick to force locales to reload
      this.lastEditedArgumentKey = this.lastEditedArgumentKey
    }
  },
  props: {
    args: Object,
    links: Array,
    modalId: String,
    templateName: String,
    editable: Boolean,
    fqdn: Array,
  },
}
</script>
