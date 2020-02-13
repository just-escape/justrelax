<template>
  <div>
    <span v-for="link in links" :key="link.key">
      <span v-if="link.type === 'text'">{{ $t('editor.links.' + templateName + '.' + link.locale) }}</span>
      <span v-else-if="link.type === 'argument'">
        <FormattedValue
          v-b-modal="getSubmodalId(link.key)"
          :value="args[link.key]"
          :editable="true"
          :editDisabled="link.value_type === 'disabled'"
          :lastEdited="lastEditedArgumentKey === link.key"
        />
        <ValueModal
          v-if="link.value_type !== 'disabled'"
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
