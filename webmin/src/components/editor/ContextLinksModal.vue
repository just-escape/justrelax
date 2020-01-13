<template>
  <div>
    <span v-for="(link, index) in contextLinks" :key="index">
      <span v-if="link.type === 'text'">{{ link.text }}</span>
      <span v-else-if="link.type === 'argument'">
        <FormattedArgument
          v-b-modal="getSubmodalId(link.argumentId)"
          :argument="link.argument"
          :editable="true"
          :lastEdited="lastEditedArgumentId === link.argumentId"
        />
        <ArgumentModal
          :modalId="getSubmodalId(link.argumentId)"
          :argument="link.argument"
          @updateArgument="(argument) => updateArgument(link.argumentId, argument)"
          @hidden="updateLastEditedArgument(link.argumentId)"
        />
      </span>
    </span>
  </div>
</template>

<script>
import FormattedArgument from '@/components/editor/FormattedArgument.vue'
import ArgumentModal from '@/components/editor/ArgumentModal.vue'

export default {
  name: "ContextLinksModal",
  components: {
    FormattedArgument,
    ArgumentModal,
  },
  data() {
    return {
      lastEditedArgumentId: undefined,
    }
  },
  methods: {
    getSubmodalId(suffix) {
      return this.modalId + '-' + suffix
    },
    updateArgument(argumentId, argument) {
      this.$emit('updateArgument', argumentId, argument)
    },
    updateLastEditedArgument(argumentId) {
      this.lastEditedArgumentId = argumentId
    },
  },
  watch: {
    contextLinks() {
      this.lastEditedArgumentId = undefined
    }
  },
  props: {
    contextLinks: Array,
  },
}
</script>
