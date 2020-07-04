<template>
  <Window :title="$t('services')">
    <div class="d-flex flex-row justify-content-around mx-4 h-100">
      <div class="d-flex flex-column align-items-center justify-content-center h-100">
        <ServiceStatus class="mb-3" :label="$t('synchronisation')">
          <i class="fas fa-project-diagram size-50 text-teal"></i>
        </ServiceStatus>
        <ServiceStatus
          class="mb-3" :label="$t('ventilation')"
          :error="blinkVentilationService"
        >
          <i
            class="fas fa-fan size-50"
            :class="{
              'text-teal': !blinkVentilationService,
              'text-red': blinkVentilationService,
            }"
          ></i>
        </ServiceStatus>
        <ServiceStatus class="mb-3" :label="$t('arm')">
          <img src="@/assets/img/robotics.png" height="53px">
        </ServiceStatus>
        <ServiceStatus :label="$t('freezer')">
          <i class="far fa-snowflake size-50 text-teal"></i>
        </ServiceStatus>
      </div>
      <div class="d-flex flex-column align-items-center justify-content-center h-100">
        <ServiceStatus class="mb-3" :label="$t('menu')">
          <img src="@/assets/img/hologram.svg" height="53px">
        </ServiceStatus>
        <ServiceStatus class="mb-3" :label="$t('stocks')">
          <i class="fas fa-cubes size-50 text-teal"></i>
        </ServiceStatus>
        <ServiceStatus class="mb-3" :label="$t('printer')">
          <img src="@/assets/img/printer.png" height="53px">
        </ServiceStatus>
        <ServiceStatus :label="$t('oven')">
          <img src="@/assets/img/oven.svg" height="53px">
        </ServiceStatus>
      </div>
    </div>
  </Window>
</template>

<script>
import Window from '@/components/Window.vue'
import ServiceStatus from '@/components/ServiceStatus.vue'
import businessStore from '@/store/businessStore.js'

export default {
  name: "ServicesWindow",
  components: {
    Window,
    ServiceStatus,
  },
  data() {
    return {
      blinkVentilationService: false,
    }
  },
  computed: {
    displayDangerWindow() {
      return businessStore.state.displayDangerWindow
    },
  },
  methods: {
    activateVentilationServiceBlink() {
      this.blinkVentilationService = true
    },
  },
  watch: {
    displayDangerWindow(newValue) {
      if (newValue) {
        setTimeout(this.activateVentilationServiceBlink, 375)
      }
    },
  },
}
</script>