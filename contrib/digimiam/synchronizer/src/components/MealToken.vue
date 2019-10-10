<template>
  <div>
    <MealTokenWire :tokenIndex="tokenIndex"/>
    <MealTokenCursor :tokenIndex="tokenIndex"/>
  </div>
</template>

<script>
import MealTokenWire from '@/components/MealTokenWire.vue'
import MealTokenCursor from '@/components/MealTokenCursor.vue'

export default {
  name: 'MealToken',
  components: {
    MealTokenWire,
    MealTokenCursor,
  },
  props: ['tokenIndex'],
}
</script>