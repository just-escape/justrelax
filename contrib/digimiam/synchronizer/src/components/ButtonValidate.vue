<template>
  <ButtonBlue
    @click="$emit('click')"
    class="btn-block"
    :disabled="disabled"
  >
    <div class="d-flex flex-row justify-content-center">
      <span class="align-self-center mr-3">{{ $t('validate') }}</span>
      <img src="@/assets/img/hologram.svg" height="24px">
    </div>
  </ButtonBlue>
</template>

<script>
import ButtonBlue from '@/components/ButtonBlue.vue'

export default {
  name: 'ButtonValidate',
  components: {
    ButtonBlue,
  },
  props: {
    disabled: {
      type: Boolean,
      default: false,
    },
  },
}
</script>
