<template>
  <b-alert show>
    <div class="d-flex flex-row">
      <div class="mr-3">
        <i class="fas fa-exclamation"></i>
      </div>
      <div class="w-100">
        <div class="d-flex justify-content-between">
          <div class="font-weight-bold">
            Something went wrong
          </div>
          <button class="d-flex align-items-center ml-3 close" @click="$emit('close')">
            <small><i class="fas fa-times"></i></small>
          </button>
        </div>
        <div class="text-grey">
          <slot></slot>
        </div>
      </div>
    </div>
  </b-alert>
</template>

<script>
export default {
  name: 'AlertMulberry',
}
</script>

<style scoped>
.alert {
  color: #cb4299;
  background-color: #3c3c3e;
  border-color: #cb4299;
  padding: 0.5rem 0.75rem;
}

.close {
  color: #cb4299;
  text-shadow: 1px 1px 0 #555;
  opacity: 0.8;
  outline-color: transparent;
}
</style>
