<template>
  <v-select
    class="inline-select"
    v-model="value"
    :options="options"
    :clearable="false"
  ></v-select>
</template>

<script>
export default {
  name: "InlineSelect",
  data() {
    return {
      value: null,
    }
  },
  created() {
    this.value = this.default
  },
  props: {
    options: Array,
    default: Promise,
  }
}
</script>

<style>
.inline-select {
  display: inline-block;
}

.inline-select .vs__search::placeholder,
.inline-select .vs__dropdown-toggle,
.inline-select .vs__dropdown-menu {
  background-color: #4d4d4f;
  border: #f8f9fa 1px solid;
  color: #f8f9fa;
}

.inline-select .vs__selected,
.inline-select .vs__search,
.inline-select .vs__dropdown-option {
  color: #f8f9fa;
}

.inline-select .vs__dropdown-toggle {
  padding-bottom: 0;
}

.inline-select .vs__search,
.inline-select .vs__search:focus,
.inline-select .vs__selected {
  margin-top: 0;
}

.inline-select .vs__actions {
  padding-top: 0;
}

.inline-select .vs__dropdown-menu {
  padding: 0;
}

.inline-select .vs__dropdown-option--highlight {
  background: #ef8649;
}

.inline-select .vs__dropdown-option,
.inline-select .vs__dropdown-option--highlight {
  line-height: 1;
}

.inline-select .vs__clear,
.inline-select .vs__open-indicator {
  fill: #f8f9fa;
}
</style>