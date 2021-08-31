<template>
  <Window :title="$t('ads')" class="h-100">
    <div class="d-flex flex-column justify-content-around mx-4 h-100">
      <div class="d-flex flex-column align-items-center">
        <div class="position-relative mb-1">
          <!-- Simulated video slot thanks to the dimensions, but there is none -->
          <div class="glowing-container video-thumbnail"/>
        </div>

        <div class="media-body">{{ $t('gaufresque.mp6') }}</div>
      </div>

      <div class="d-flex flex-column align-items-center">
        <div class="position-relative mb-1">
          <!-- Simulated video slot thanks to the dimensions, but there is none -->
          <div class="glowing-container video-thumbnail"/>
        </div>

        <div class="media-body">{{ $t('zéphyr_3000 (1).mp6') }}</div>
      </div>

      <div class="d-flex flex-column align-items-center" style="filter: grayscale(1)">
        <div class="position-relative mb-1">
          <div class="glowing-container video-thumbnail" style="border-style: dashed"/>
        </div>

        <div class="media-body" style="font-style: italic; color: gray">Slot vide</div>
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