<template>
  <div>
    <span v-for="link in links" :key="link.key">
      <span v-if="link.type === 'text'">{{ $t('editor.links.' + templateName + '.' + link.locale) }}</span>
      <span v-else-if="link.type === 'argument'">
        <FormattedValue
          v-b-modal="getSubmodalId(link.key)"
          :value="args[link.key]"
          :editable="true"
          :editDisabled="isEditDisabled(link)"
          :lastEdited="lastEditedArgumentKey === link.key"
        />
        <ValueModal
          v-if="!isEditDisabled(link)"
          :modalId="getSubmodalId(link.key)"
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
  name: "TemplateEditable",
  components: {
    FormattedValue,
    ValueModal,
  },
  data() {
    return {
      lastEditedArgumentKey: undefined,
    }
  },
  methods: {
    getSubmodalId(suffix) {
      return this.modalId + '-' + suffix
    },
    updateArgument(key, value) {
      this.$emit('updateArgument', key, value)
    },
    updateLastEditedArgument(argumentKey) {
      this.lastEditedArgumentKey = argumentKey
    },
    isEditDisabled(link) {
      return link.value_type === 'disabled' || (link.value_type === 'variable' && editorStore.state.variables.length === 0)
    },
  },
  watch: {
    links() {
      this.lastEditedArgumentKey = undefined
    }
  },
  props: {
    args: Object,
    links: Array,
    modalId: String,
    templateName: String,
  },
}
</script>
