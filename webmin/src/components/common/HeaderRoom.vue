<template>
  <div class="d-flex flex-column">
    <div
      v-for="room in rooms"
      :key="room.id"
    >
        <DigimiamToolbar
            v-if="room.toolbar === 'digimiam'"
            :url="'/rooms/' + room.id + '/live'"
            :name="room.name"
            :roomId="room.id"
            :defaultPublicationChannel="room.default_publication_channel"
            class="my-1"
        ></DigimiamToolbar>
        <LinkToolbar v-else
            :url="'/rooms/' + room.id + '/live'"
            :name="room.name"
            :roomId="room.id"
            class="my-1"
        >
        </LinkToolbar>
    </div>
  </div>
</template>

<script>
import DigimiamToolbar from '@/components/common/DigimiamToolbar.vue'
import LinkToolbar from '@/components/common/LinkToolbar.vue'
import roomStore from '@/store/roomStore.js'

export default {
  name: 'HeaderRoom',
  components: {
    DigimiamToolbar,
    LinkToolbar,
  },
  computed: {
    rooms() {
      return roomStore.state.rooms ? roomStore.state.rooms : []
    }
  },
}
</script>