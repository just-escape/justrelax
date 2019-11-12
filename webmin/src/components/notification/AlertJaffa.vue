<template>
  <b-alert show>
    <div class="d-flex flex-row">
      <div class="align-self-center mr-3">
        <i class="fas fa-info"></i>
      </div>
      <div class="w-100">
        <button class="d-flex align-items-center h-100 ml-3 close" @click="$emit('close')">
          <small><i class="fas fa-times"></i></small>
        </button>
        <div>
          <slot></slot>
        </div>
      </div>
    </div>
  </b-alert>
</template>

<script>
export default {
  name: 'AlertJaffa',
  props: ['notification'],
}
</script>

<style scoped>
.alert {
  color: #f38d40;
  background-color: #3c3c3e;
  border-color: #f38d40;
  padding: 0.5rem 0.75rem;
}

.close {
  color: #f38d40;
  text-shadow: 1px 1px 0 #555;
  opacity: 0.8;
  outline-color: transparent;
}
</style>
