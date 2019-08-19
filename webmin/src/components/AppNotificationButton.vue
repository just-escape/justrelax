<template>
  <div class="position-relative">
    <div v-if="this.notifications.length > 0" :class="'position-absolute count' + this.fontSize">
      {{ this.countText }}
    </div>
    <ButtonMulberry :active="this.notifications.length > 0" @click="toggleDisplayNotificationPanel()">
      <i class="fas fa-bell"></i>
    </ButtonMulberry>
  </div>
</template>

<script>
import ButtonMulberry from '@/components/ButtonMulberry.vue'
import notificationStore from '@/store/notificationStore.js'
import preferenceStore from '@/store/preferenceStore.js'

export default {
  name: 'AppNotificationButton',
  components: {
    ButtonMulberry
  },
  computed: {
    notifications: function() {
      return notificationStore.state.notifications
    },
    countText: function() {
      if (this.notifications.length > 10) {
        return '10+'
      } else {
        return notificationStore.state.notifications.length
      }
    },
    fontSize: function() {
      if (this.notifications.length > 10) {
        return ' size-06'
      } else {
        return ' size-07'
      }
    }
  },
  methods: {
    toggleDisplayNotificationPanel: function() {
      preferenceStore.dispatch('toggleDisplayNotificationPanel')
    }
  }
}
</script>

<style scoped>
.count {
  right: 3px;
  bottom: 3px;
  line-height: 1;
  color: #3c3c3e;
}

.size-06 {
  font-size: 0.6rem;
}

.size-07 {
  font-size: 0.7rem;
}
</style>
