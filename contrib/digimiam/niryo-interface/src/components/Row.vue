<template>
  <div class="d-flex flex-row justify-content-center align-items-center">
    <Timer :timeUnits="timeUnits" class="mr-5"/>
    <div class="d-flex mr-5">
      {{ title }}
    </div>
    <div class="d-flex flex-row">
      <Token
        v-for="(t, index) in tokens"
        :key="t"
        class="mr-4"
        :selected="selectedTokenIndex === index"
        :selectionError="selectionError"
        :configurationId="t"
        :goodToken="t === goodToken && cheatEnabled"
        @click="onClick(index)"
      />
    </div>
  </div>
</template>

<script>
import Timer from '@/components/Timer.vue'
import Token from '@/components/Token.vue'

export default {
  name: 'Row',
  components: {
    Timer,
    Token,
  },
  methods: {
    onClick(index) {
      this.$emit('tokenClicked', index)
    }
  },
  props: {
    title: String,
    tokens: Array,
    selectedTokenIndex: Number,
    timeUnits: Array,
    selectionError: Boolean,
    goodToken: String,
    cheatEnabled: Boolean,
  },
}
</script>
