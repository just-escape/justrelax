<template>
  <div>
    <span v-for="(link, index) in contextLinks" :key="index">
      <span v-if="link.type === 'text'">{{ link.text }}</span>
      <span v-else-if="link.type === 'argument'">
        <FormattedArgument :argument="link.argument"/>
      </span>
    </span>
  </div>
</template>

<script>
import FormattedArgument from '@/components/editor/FormattedArgument.vue'

export default {
  name: "ContextLinksLine",
  components: {
    FormattedArgument,
  },
  props: {
    contextLinks: Array,
  },
}
</script>
