<template>
  <ButtonBlue class="btn-block">
    <div class="d-flex flex-row justify-content-center">
      <span class="align-self-center mr-3">{{ $t('activate') }}</span>
      <img src="@/assets/img/hologram.svg" height="24px">
    </div>
  </ButtonBlue>
</template>

<script>
import ButtonBlue from '@/components/ButtonBlue.vue'

export default {
  name: 'ButtonDisplay',
  components: {
    ButtonBlue,
  },
}
</script>
