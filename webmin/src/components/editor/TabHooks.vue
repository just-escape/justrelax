<template>
  <div>
    <div class="row mb-3">
      <div class="col-6">
        <label class="typo__label">Start actions</label>
        <ActionSelector :initialActions="[]" />
      </div>
    </div>
    <div class="row mb-5">
      <div class="col-6">
        <label class="typo__label">Reset actions</label>
        <ActionSelector :initialActions="[]" />
      </div>
    </div>
  </div>
</template>

<script>
import ActionSelector from '@/components/editor/ActionSelector.vue'

export default {
  name: 'TabHooks',
  components: {
    ActionSelector
  },
}
</script>
