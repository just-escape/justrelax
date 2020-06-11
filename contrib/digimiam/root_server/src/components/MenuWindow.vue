<template>
  <Window :title="$t('MENU')">
    <div class="d-flex flex-row justify-content-around mx-4 h-100">
      <div class="d-flex flex-column align-items-center justify-content-center h-100">
        <ServiceStatus class="mb-3" :label="'?'">
          <i class="fas fa-question size-50 text-teal"></i>
        </ServiceStatus>
        <ServiceStatus class="mb-3" :label="'?'">
          <i class="fas fa-question size-50 text-teal"></i>
        </ServiceStatus>
        <ServiceStatus class="mb-3" :label="'?'">
          <i class="fas fa-question size-50 text-teal"></i>
        </ServiceStatus>
        <ServiceStatus class="mb-3" :label="'?'">
          <i class="fas fa-question size-50 text-teal"></i>
        </ServiceStatus>
      </div>
      <div class="d-flex flex-column align-items-center justify-content-center h-100">
        <ServiceStatus class="mb-3" :label="'?'">
          <i class="fas fa-question size-50 text-teal"></i>
        </ServiceStatus>
        <ServiceStatus class="mb-3" :label="'?'">
          <i class="fas fa-question size-50 text-teal"></i>
        </ServiceStatus>
        <ServiceStatus class="mb-3" :label="'?'">
          <i class="fas fa-question size-50 text-teal"></i>
        </ServiceStatus>
        <ServiceStatus class="mb-3" :label="'?'">
          <i class="fas fa-question size-50 text-teal"></i>
        </ServiceStatus>
      </div>
    </div>
  </Window>
</template>

<script>
import Window from '@/components/Window.vue'
import ServiceStatus from '@/components/ServiceStatus.vue'

export default {
  name: "ServicesWindow",
  components: {
    Window,
    ServiceStatus,
  },
  data() {
    return {
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
}
</script>