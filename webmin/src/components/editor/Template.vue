<template>
  <div>
    <span v-for="(link, index) in links" :key="index">
      <span v-if="link.type === 'text'">{{ link.text }}</span>
      <span v-else-if="link.type === 'argument'">
        <FormattedValue :value="args[link.key]"/>
      </span>
    </span>
  </div>
</template>

<script>
import FormattedValue from '@/components/editor/FormattedValue.vue'

export default {
  name: "Template",
  components: {
    FormattedValue,
  },
  props: {
    args: Object,
    links: Array,
  },
}
</script>