<template>
  <AppContent>
    <div slot="main">
      <Cameras :roomId="room.id"/>
      <PublishEvent v-if="isInMaintenanceMode" :defaultChannel="room.default_publication_channel" class="mb-4"/>
      <Actions :roomId="room.id"/>
    </div>
  </AppContent>
</template>

<script>
import AppContent from '@/components/common/AppContent.vue'
import Cameras from '@/components/live/Cameras.vue'
import PublishEvent from '@/components/live/PublishEvent.vue'
import Actions from '@/components/live/Actions.vue'
import roomStore from '@/store/roomStore.js'
import preferenceStore from '@/store/preferenceStore.js'

export default {
  name: 'PageLive',
  components: {
    AppContent,
    Cameras,
    PublishEvent,
    Actions,
  },
  computed: {
    isInMaintenanceMode() {
      return preferenceStore.state.isInMaintenanceMode
    },
    room() {
      if (roomStore.state.rooms === undefined) {
        return undefined
      }

      var parsedRoomId = parseInt(this.roomId, 10)
      if (Number.isNaN(parsedRoomId)) {
        return null
      }

      for (var room of roomStore.state.rooms) {
        if (room.id === parsedRoomId) {
          return room
        }
      }

      return null
    },
  },
  props: ['roomId']
}
</script>
