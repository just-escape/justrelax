<template>
  <div>
    <span v-for="link in links" :key="link.key">
      <span v-if="link.link_type === 'text'">{{ link.text }}</span>
      <span v-else-if="link.link_type === 'argument'">
        <FormattedArgument
          v-b-modal="getSubmodalId(link.key)"
          :argument="args[link.key]"
          :editable="true"
          :lastEdited="lastEditedArgumentKey === link.key"
        />
        <ArgumentModal
          :modalId="getSubmodalId(link.key)"
          :argument="args[link.key]"
          @updateArgument="(argument) => updateArgument(link.key, argument)"
          @hidden="updateLastEditedArgumentKey(link.key)"
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
      lastEditedArgumentKey: undefined,
    }
  },
  methods: {
    getSubmodalId(suffix) {
      return this.modalId + '-' + suffix
    },
    updateArgument(argumentKey, argument) {
      this.$emit('updateArgument', argumentKey, argument)
    },
    updateLastEditedArgumentKey(argumentKey) {
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
  },
}
</script>
