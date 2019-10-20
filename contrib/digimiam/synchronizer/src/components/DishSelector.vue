<template>
  <div>
    <DishSelectorWire :itemIndex="itemIndex"/>
    <DishSelectorCursor :itemIndex="itemIndex"/>
  </div>
</template>

<script>
import DishSelectorWire from '@/components/DishSelectorWire.vue'
import DishSelectorCursor from '@/components/DishSelectorCursor.vue'

export default {
  name: 'DishSelector',
  components: {
    DishSelectorWire,
    DishSelectorCursor,
  },
  props: ['itemIndex'],
}
</script>