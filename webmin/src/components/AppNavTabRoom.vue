<template>
  <div>
    <div class="d-flex flex-row justify-content-between p-3">
      <span>
        <i class="text-jaffa fas fa-door-open fa-fw fa-lg mr-3"></i>Rooms
      </span>
      <div>
        <CollapseChevron v-b-toggle="'collapse-rooms'"/>
      </div>
    </div>
    <b-collapse id="collapse-rooms" visible>
      <ul v-if="displayRooms" class="list-unstyled mb-0">
        <li
          v-for="r in rooms"
          :key="r.id"
          class="bgc-dark"
        >
          <a :href="'/rooms/' + r.id">
            <div class="p-3 pl-4 d-flex flex-row justify-content-between">
              <span>
                {{ r.scenario }}<span v-if="r.cardinal"> - {{ r.cardinal }}</span>
              </span>
              <TicksClock :ticks="r.liveData.ticks" :displayZero="false"/>
            </div>
          </a>
        </li>
      </ul>
      <ul v-else class="list-unstyled mb-0">
        <li class="font-italic p-3 pl-4 bgc-dark">
          No rooms available
        </li>
      </ul>
    </b-collapse>
  </div>
</template>

<script>
import CollapseChevron from '@/components/CollapseChevron.vue'
import TicksClock from '@/components/TicksClock.vue'
import roomStore from '@/store/roomStore.js'

export default {
  name: 'AppNavTabRoom',
  components: {
    CollapseChevron,
    TicksClock
  },
  computed: {
    rooms() {
      return roomStore.state.rooms
    },
    displayRooms() {
      return !(Object.entries(this.rooms).length === 0 && this.rooms.constructor === Object)
    }
  }
}
</script>

<style scoped>
ul > li {
  border-bottom: 1px solid #2e2e2e;
}

ul > li:last-child {
  border-bottom: 0;
}
</style>