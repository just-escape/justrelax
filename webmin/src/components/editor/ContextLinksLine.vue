<template>
  <div>
    <span v-for="(link, index) in contextLinks" :key="index">
      <span v-if="link.type === 'text'">{{ link.text }}</span>
      <span v-else-if="link.type === 'argument'">
        <Argument :argument="link.argument"/>
      </span>
    </span>
  </div>
</template>

<script>
import Argument from '@/components/editor/Argument.vue'

export default {
  name: "ContextLinksLine",
  components: {
    Argument,
  },
  props: {
    contextLinks: Array,
  },
}
</script>
