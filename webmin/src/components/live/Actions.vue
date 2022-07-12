<template>
  <div>
    <div class="d-flex flex-row justify-content-end">
      <div class="d-flex justify-content-end">
        <div class="min-width-100px mr-1 mb-1">
          <b-form-select
            class="form-control"
            v-model="selected"
            :options="{
              'd1.scenario': 'Digimiam zone 1',
              'd2.scenario': 'Digimiam zone 2',
              'digimiam.scenario': 'Digimiam zone 1 et 2',
            }"
            :html="true"
          />
        </div>
      </div>
    </div>
    <div class="container-fluid">
      <div v-if="cards === undefined">
        Loading...
      </div>
      <div v-else class="row">
        <div
          v-for="card in cards"
          :key="card.id"
          class="col-12 col-lg-6 col-xl-3 mb-1 px-1"
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
import roomStore from '@/store/roomStore.js'

export default {
  name: 'Actions',
  components: {
    ActionCard
  },
  data() {
    return {
      cards: undefined,
      selected: null,
    }
  },
  watch: {
    selected(newValue) {
      roomStore.commit(
        'setRoomDefaultPublicationChannel',
        {roomId: this.roomId, defaultPublicationChannel: newValue}
      )
    },
  },
  created() {
    for (var room of roomStore.state.rooms) {
      if (room.id == this.roomId) {
        this.selected = room.default_publication_channel
      }
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
