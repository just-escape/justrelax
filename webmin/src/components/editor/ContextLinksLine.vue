<template>
  <div>
    <span v-for="(link, index) in links" :key="index">
      <span v-if="link.link_type === 'text'">{{ link.text }}</span>
      <span v-else-if="link.link_type === 'argument'">
        <FormattedArgument :argument="args[link.key]"/>
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
    args: Object,
    links: Array,
  },
}
</script>
