<template>
  <Window :title="$t('configuration')" class="h-100">
    <div class="d-flex h-100">
      <div class="d-flex flex-column lh-1 mx-4 justify-content-center h-100 w-100">
        <div class="d-flex flex-row mb-5">
            <div>{{ $t('mode') }}</div>
            <span class="underline-dots flex-grow-1 mx-1"></span>
            <div><span class="opacity-25">{{ $t('marmitron') }}</span> / {{ $t('manual') }}</div>
        </div>
        <div class="d-flex flex-row mb-3">
            <div>{{ $t('security') }}</div>
            <span class="underline-dots flex-grow-1 mx-1"></span>
            <div>{{ $t('on') }} / <span class="opacity-25">{{ $t('off') }}</span></div>
        </div>
        <div class="d-flex flex-row mb-3">
            <div>{{ $t('ongoing_maintenance') }}</div>
            <span class="underline-dots flex-grow-1 mx-1"></span>
            <div>{{ $t('yes') }} / <span class="opacity-25">{{ $t('no') }}</span></div>
        </div>
        <div class="d-flex flex-row mb-5">
            <div>{{ $t('open') }}</div>
            <span class="underline-dots flex-grow-1 mx-1"></span>
            <div><span class="opacity-25">{{ $t('yes') }}</span> / {{ $t('no') }}</div>
        </div>
        <div class="d-flex flex-row mb-3">
            <div>{{ $t('supply') }}</div>
            <span class="underline-dots flex-grow-1 mx-1"></span>
            <div>{{ $t('marmitron') }} / <span class="opacity-25">{{ $t('manual') }}</span></div>
        </div>
        <div class="d-flex flex-row mb-3">
            <div>{{ $t('food_hydroinflation') }}</div>
            <span class="underline-dots flex-grow-1 mx-1"></span>
            <div>{{ $t('yes') }} / <span class="opacity-25">{{ $t('no') }}</span></div>
        </div>
        <div class="d-flex flex-row">
            <div>{{ $t('air_quality') }}</div>
            <span class="underline-dots flex-grow-1 mx-1"></span>
            <div><span class="opacity-25">{{ $t('optimal') }}</span> / {{ $t('economic') }}</div>
        </div>
      </div>
    </div>
  </Window>
</template>

<script>
import Window from '@/components/Window.vue'

export default {
  name: "ConfigurationWindow",
  components: {
    Window,
  }
}
</script>

<style scoped>
.underline-dots {
  font-size: 18px;
  border-bottom: 1px dotted #ffffff;
  margin-bottom: 3px;
}

.opacity-25 {
  opacity: 0.25;
}
</style>