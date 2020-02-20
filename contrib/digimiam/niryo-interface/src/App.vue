<template>
  <div id="app" class="h-100">
    <div class="d-flex flex-column justify-content-around h-100">
      <Row
        v-for="(row, index) in rows"
        :key="index"
        :title="row.title"
        :timeUnits="row.timeUnits"
        :tokens="row.tokens"
        :selectedTokenIndex="row.selectedTokenIndex"
        :selectionError="row.selectionError"
        :goodToken="row.goodToken"
        :cheatEnabled="cheatEnabled"
        @tokenClicked="(tokenIndex) => onTokenClicked(index, tokenIndex)"
      />
    </div>
  </div>
</template>

<script>
import Row from '@/components/Row.vue'
import businessStore from '@/store/businessStore.js'

export default {
  name: 'App',
  components: {
    Row,
  },
  computed: {
    rows() {
      return businessStore.state.rows
    },
    cheatEnabled() {
      return businessStore.state.cheatEnabled
    },
  },
  methods: {
    onTokenClicked(rowIndex, tokenIndex) {
      businessStore.commit('setSelectedToken', {rowIndex, tokenIndex})
    },
  },
  created() {
    this.$connect()
    setTimeout(businessStore.dispatch, 300, 'startGame')
  }
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}
</style>
