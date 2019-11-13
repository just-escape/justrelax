<template>
  <div>
    {{ action }}
  </div>
</template>

<script>
export default {
  name: "Action",
  props: {
    action: Object,
  }
}
</script>
