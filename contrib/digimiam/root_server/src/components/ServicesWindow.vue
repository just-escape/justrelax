<template>
  <Window :title="$t('SERVICES')">
    <div class="d-flex flex-row justify-content-around mx-4 h-100">
      <div class="d-flex flex-column align-items-center justify-content-center h-100">
        <ServiceStatus class="mb-3" :label="'Synchronisation'">
          <i class="fas fa-project-diagram size-50 text-teal"></i>
        </ServiceStatus>
        <ServiceStatus
          class="mb-3" :label="'Ventilation'"
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
        <ServiceStatus class="mb-3" :label="'Bras'">
          <img src="@/assets/robotics.png" height="53px">
        </ServiceStatus>
        <ServiceStatus :label="'Congélateur'">
          <i class="far fa-snowflake size-50 text-teal"></i>
        </ServiceStatus>
      </div>
      <div class="d-flex flex-column align-items-center justify-content-center h-100">
        <ServiceStatus class="mb-3" :label="'Menu'">
          <img src="@/assets/hologram.svg" height="53px">
        </ServiceStatus>
        <ServiceStatus class="mb-3" :label="'Stocks'">
          <i class="fas fa-cubes size-50 text-teal"></i>
        </ServiceStatus>
        <ServiceStatus class="mb-3" :label="'Imprimante'">
          <img src="@/assets/printer.png" height="53px">
        </ServiceStatus>
        <ServiceStatus :label="'Four'">
          <img src="@/assets/oven.svg" height="53px">
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
      services: [
        [
          {
            label: "Synchronisation",
            picture: '<i class="fas fa-project-diagram fa-fw size-50 text-teal"></i>',
          },
          {
            label: "Synchronisation",
            picture: '<i class="fas fa-project-diagram fa-fw size-50 text-teal"></i>',
          },
          {
            label: "Synchronisation",
            picture: '<i class="fas fa-project-diagram fa-fw size-50 text-teal"></i>',
          },
          {
            label: "Synchronisation",
            picture: '<i class="fas fa-project-diagram fa-fw size-50 text-teal"></i>',
          },
        ],
        [
          {
            label: "Menu",
            picture: '',
          },
          {
            label: "Synchronisation",
            picture: '<i class="fas fa-project-diagram fa-fw size-50 text-teal"></i>',
          },
          {
            label: "Synchronisation",
            picture: '<i class="fas fa-project-diagram fa-fw size-50 text-teal"></i>',
          },
          {
            label: "Synchronisation",
            picture: '<i class="fas fa-project-diagram fa-fw size-50 text-teal"></i>',
          },
        ],
      ]
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