<template>
  <div
    class="w-100"
    :class="{'bg-active': !gameLost && active, 'bg-inactive': !active, 'bg-red': gameLost && active}"
    style="height: 20px;"
  ></div>
</template>

<script>
import businessStore from '@/store/businessStore.js'

export default {
  name: "TimeUnit",
  computed: {
    gameLost() {
      return businessStore.state.gameLost
    }
  },
  props: {
    active: Boolean,
  }
}
</script>

<style scoped>
.bg-active {
  background: blue;
}

.bg-inactive {
  background: lightgrey;
}

.bg-red {
  background: red;
}
</style>