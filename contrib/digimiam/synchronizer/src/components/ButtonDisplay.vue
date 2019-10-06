<template>
  <ButtonBlue>
    <div class="d-flex flex-row">
      <span class="align-self-center mr-2">DISPLAY</span>
      <img src="@/assets/img/hologram.svg" height="22px">
    </div>
  </ButtonBlue>
</template>

<script>
import ButtonBlue from '@/components/ButtonBlue.vue'

export default {
  name: 'ButtonDisplay',
  components: {
    ButtonBlue
  },
}
</script>
