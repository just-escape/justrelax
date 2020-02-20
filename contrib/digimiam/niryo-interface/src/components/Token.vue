<template>
  <div
    class="pointer bordered pl-1 pt-1"
    :class="{'border-green': selected && !selectionError, 'border-red': selected && selectionError}"
    @click="onClick()"
  >
    <div
      v-for="(c, cIndex) in configuration"
      :key="cIndex"
      class="d-flex flex-row pb-1"
    >
      <div
        v-for="(r, rIndex) in c"
        :key="rIndex"
        class="d-flex flex-column mr-1"
        :class="{'bg-black': !goodToken && r, 'bg-grey': !r, 'bg-green': goodToken && r}"
        style="width: 15px; height: 15px"
      >
      </div>
    </div>
  </div>
</template>

<script>
import businessStore from '@/store/businessStore.js'

export default {
  name: "Token",
  computed: {
    configuration() {
      return businessStore.state.configurations[this.configurationId]
    },
  },
  methods: {
    onClick() {
      this.$emit('click')
    },
  },
  props: {
    configurationId: String,
    selected: Boolean,
    selectionError: Boolean,
    goodToken: Boolean,
  },
}
</script>

<style scoped>
.pointer:hover {
  cursor: pointer;
}

.bordered {
  border: 3px solid transparent;
}

.border-green {
  border-color: green;
}

.border-red {
  border-color: red;
}

.bg-black {
  background: black;
}

.bg-grey {
  background: lightgrey;
}

.bg-green {
  background-color: green;
}
</style>