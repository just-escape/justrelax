<template>
  <ButtonBlue
    @click="$emit('click')"
    class="btn-block"
    :disabled="disabled"
  >
    <div class="d-flex flex-row justify-content-center">
      <span class="align-self-center mr-3">{{ $t('validate') }}</span>
      <!-- Validation no longer changes menu items, it is done each time an item is changed. This icon is no longer useful, but I keep the line just in case we need it elsewhere... -->
      <!--<img src="@/assets/img/hologram.svg" height="24px">-->
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
