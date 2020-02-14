<template>
  <span
    :class="{
      pointer: editable && !editDisabled,
      'text-jaffa': editable && !editDisabled,
      'text-disabled': editDisabled,
      'text-underline': editable,
      'text-double': lastEdited,
      'font-italic': !editable,
    }"
  >
    <span>{{ formattedContent }}</span>
  </span>
</template>

<script>
export default {
  name: "FormattedValue",
  props: {
    formattedContent: {
      type: String,
      default: "",
    },
    editable: {
      type: Boolean,
      default: false,
    },
    editDisabled: {
      type: Boolean,
      default: false,
    },
    lastEdited: {
      type: Boolean,
      default: false,
    }
  },
}
</script>

<style scoped>
.text-double {
  text-decoration-style: double;
}

.text-disabled {
  opacity: 0.5;
}
</style>
