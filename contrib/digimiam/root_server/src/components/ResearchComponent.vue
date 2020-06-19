<template>
  <div v-html="possibilities[currentSearchIndex]"/>
</template>

<script>
export default {
  name: "ResearchComponent",
  data() {
    return {
      currentSearchIndex: 0,
      searchDelay: 100,
      probabilityToFind: 0,
    }
  },
  methods: {
    search() {
      if (Math.random() > this.probabilityToFind) {
        this.searchDelay += 30
        this.probabilityToFind += 0.01
        this.currentSearchIndex = Math.floor(Math.random() * this.possibilities.length)
        setTimeout(this.search, Math.random() * this.searchDelay)
      } else {
        this.$emit('stop')
      }
    },
  },
  watch: {
    shuffleSignal() {
      this.searchDelay = 100
      this.probabilityToFind = 0
      setTimeout(this.search, Math.random() * this.searchDelay)
    },
  },
  props: {
    possibilities: Array,
    shuffleSignal: Boolean,
  }
}
</script>