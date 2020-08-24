<template>
  <div>
    <h2 class="big-noodle text-jaffa text-center">Actions</h2>
    <div v-if="displayCards" class="container-fluid">
      <div class="row">
        <div
          v-for="card in room.cards"
          :key="card.id"
          class="col-12 col-lg-6 col-xl-3 mb-4"
        >
          <ActionCard
            :roomId="room.id"
            :card="card"
          />
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import ActionCard from '@/components/live/ActionCard.vue'
import roomStore from '@/store/roomStore.js'

export default {
  name: 'Actions',
  components: {
    ActionCard
  },
  computed: {
    displayCards() {
      return this.room.cards !== undefined
    },
  },
  created() {
    roomStore.dispatch('fetchActions', this.room.id)
  },
  props: ['room']
}
</script>
