<template>
  <Window :title="$t('ads')" class="h-100">
    <div class="d-flex flex-column justify-content-around mx-4 h-100">
      <div class="d-flex flex-column align-items-center">
        <div class="position-relative mb-1">
          <!-- Simulated video slot thanks to the dimensions, but there is none -->
          <div class="glowing-container video-thumbnail"/>
        </div>

        <div class="media-body">{{ $t('succulente_gaufresque.mp6') }}</div>
      </div>

      <div class="d-flex flex-column align-items-center">
        <div class="position-relative mb-1">
          <!-- Simulated video slot thanks to the dimensions, but there is none -->
          <div class="glowing-container video-thumbnail"/>
        </div>

        <div class="media-body">{{ $t('zéphyr_3000_version_épurée.mp6') }}</div>
      </div>

      <div class="d-flex flex-column align-items-center">
        <div class="position-relative mb-1">
          <video src="@/assets/videos/zephyr_3000.mp4" class="glowing-container video-thumbnail"/>
          <b-btn class="position-absolute lh-1 bottom-right" size="sm" variant="outline-info">
            <i class="text-teal fas fa-expand"/>
          </b-btn>
        </div>

        <div class="media-body">{{ $t('soda wonka (muet).mp6') }}</div>
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