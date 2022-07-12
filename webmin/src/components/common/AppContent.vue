<template>
  <div class="d-flex flex-column flex-grow-1">
    <header class="bgc-dark">
      <HeaderRoom class="container-fluid h-100"></HeaderRoom>
    </header>
    <main class="d-flex flex-row h-100">
      <div class="container-fluid padding-bottom-10rem px-0">
        <slot name="main"></slot>
      </div>
    </main>
  </div>
</template>

<script>
import HeaderRoom from "@/components/common/HeaderRoom.vue"

export default {
  name: 'AppContent',
  components: {
    HeaderRoom,
  }
}
</script>

<style scoped>
header {
  z-index: 1;
  box-shadow: 0 0.1rem 0.4rem #2e2e2e;
}

main {
  overflow: hidden;
}
</style>
