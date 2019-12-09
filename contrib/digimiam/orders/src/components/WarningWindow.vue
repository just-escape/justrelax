<template>
  <div class="d-flex flex-column h-100">
    <div class="d-flex flex-row rounded-top bg-dark shadow-box-dark-top">
      <NeonsWarning class="ml-2"/>
      <h3 class="size-12 py-1 mx-3 mb-0 text-warning">ERROR</h3>
      <NeonsWarning class="mr-2"/>
    </div>
    <div class="border-left-bottom-right shadow-box-dark p-3">
      <div class="media">
        <div class="mr-3 bg-dark align-self-center d-flex justify-content-center align-items-center" style="width: 50px; height: 50px; border-radius: 50%">
          <i class="fas fa-exclamation" style="color: var(--warning);font-size: 1.7rem;"></i>
        </div>
        <div class="media-body">
          Erreur ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore.
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import NeonsWarning from "@/components/NeonsWarning.vue"

export default {
  name: "WarningWindow",
  components: {
    NeonsWarning,
  },
}
</script>

<style scoped>
.border-left-bottom-right {
  border: 3px solid var(--dark);
  border-top: 0px;
  border-bottom-left-radius: 0.25rem;
  border-bottom-right-radius: 0.25rem;
}

.shadow-box-dark-top {
  box-shadow: 1px -1px 5px var(--dark);
}
</style>
