<template>
  <div>
    <h2 class="big-noodle text-jaffa text-center">Actions</h2>
    <div class="container-fluid">
      <div v-if="cards === undefined">
        Loading...
      </div>
      <div v-else class="row">
        <div
          v-for="card in cards"
          :key="card.id"
          class="col-12 col-lg-6 col-xl-3 mb-4"
        >
          <ActionCard
            :roomId="roomId"
            :card="card"
          />
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import ActionCard from '@/components/live/ActionCard.vue'
import notificationStore from '@/store/notificationStore.js'

export default {
  name: 'Actions',
  components: {
    ActionCard
  },
  data() {
    return {
      cards: undefined,
    }
  },
  mounted() {
    let this_ = this
    this.$justRestAPI.get('/get_cards_from_room_id/?room_id=' + this.roomId)
      .then(function (response) {
        this_.cards = response.data
      })
      .catch(function (error) {
        notificationStore.dispatch('pushError', 'Error while fetching cards: ' + error)
      })
  },
  props: ['roomId']
}
</script>
