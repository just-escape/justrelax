<template>
  <div :class="'notification-panel width-300px' + collapsePanel">
    <div class="container-fluid border-left-dark pt-2 width-300px h-100">
      <h2 class="big-noodle text-center">Notifications</h2>
      <AlertMulberry v-for="n in notifications" :key="n.id" @close="clear(n.id)">
        {{ n.content }}
      </AlertMulberry>
    </div>
  </div>
</template>

<script>
import AlertMulberry from '@/components/AlertMulberry.vue'
import preferenceStore from '@/store/preferenceStore.js'
import notificationStore from '@/store/notificationStore.js'

export default {
  name: 'AppNotificationPanel',
  components: {
    AlertMulberry
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
