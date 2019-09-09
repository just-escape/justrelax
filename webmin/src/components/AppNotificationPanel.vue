<template>
  <div :class="'notification-panel width-300px' + collapsePanel">
    <div class="container-fluid border-left-dark pt-2 padding-bottom-10rem width-300px h-100">
      <h2 class="big-noodle text-center">Notifications</h2>
      <div v-for="n in notifications" :key="n.id">
        <AlertMulberry v-if="n.type == 'error'" @close="clear(n.id)">
          {{ n.message }}
        </AlertMulberry>
        <AlertJaffa v-else @close="clear(n.id)">
          {{ n.message }}
        </AlertJaffa>
      </div>
    </div>
  </div>
</template>

<script>
import AlertMulberry from '@/components/AlertMulberry.vue'
import AlertJaffa from '@/components/AlertJaffa.vue'
import preferenceStore from '@/store/preferenceStore.js'
import notificationStore from '@/store/notificationStore.js'

export default {
  name: 'AppNotificationPanel',
  components: {
    AlertMulberry,
    AlertJaffa,
  },
  computed: {
    notifications() {
      return notificationStore.state.notifications
    },
    clear() {
      return function (id) {
        notificationStore.dispatch('clearNotification', id)
      }
    },
    collapsePanel() {
      if (preferenceStore.state.displayNotificationPanel) {
        return ''
      } else {
        return ' collapse-panel'
      }
    }
  }
}
</script>

<style scoped>
.notification-panel {
  transition: all 0.35s ease;
}

.width-300px {
  width: 300px;
}

.collapse-panel {
  width: 0;
}

.border-left-dark {
  border-left: 5px solid #3c3c3e;
}
</style>
