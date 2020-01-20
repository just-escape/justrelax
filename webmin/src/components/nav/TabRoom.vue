<template>
  <div>
    <div class="d-flex flex-row justify-content-between p-3">
      <div>
        <a :href="'/rooms/' + room.id + '/live'">
          <i class="text-jaffa fas fa-door-open fa-fw fa-lg mr-3"></i>{{ getDisplayName }}
        </a>
      </div>
      <div class="d-flex flex-row">
        <TicksClock class="mr-2" :ticks="room.liveData.ticks" :displayZero="false"/>
        <CollapseChevron class="align-self-center" v-b-toggle="'collapse-rooms-' + room.id"/>
      </div>
    </div>
    <b-collapse :id="'collapse-rooms-' + room.id" :visible="isVisible">
      <ul class="list-unstyled mb-0">
        <li class="bgc-dark">
          <Tab :url="'/rooms/' + room.id + '/scores'" :icon="'far fa-id-card'" :label="'Scores'"/>
        </li>
        <li class="bgc-dark">
          <Tab :url="'/rooms/' + room.id + '/stats'" :icon="'far fa-chart-bar'" :label="'Statistics'"/>
        </li>
        <li class="bgc-dark">
          <Tab :url="'/rooms/' + room.id + '/editor'" :icon="'far fa-file-code'" :label="'Editor'"/>
        </li>
        <!--<li class="bgc-dark">
          <Tab :url="'/rooms/' + room.id + '/settings'" :icon="'fas fa-cog'" :label="'Settings'"/>
        </li>-->
      </ul>
    </b-collapse>
  </div>
</template>

<script>
import Tab from '@/components/nav/Tab.vue'
import CollapseChevron from '@/components/common/CollapseChevron.vue'
import TicksClock from '@/components/common/TicksClock.vue'
import { getRoomDisplayName } from '@/helper/room.js'

export default {
  name: 'TabRoom',
  components: {
    CollapseChevron,
    TicksClock,
    Tab,
  },
  computed: {
    getDisplayName: function() {
      return getRoomDisplayName(this.room)
    },
    isVisible: function() {
      return this.$route.params.roomId == this.room.id
    },
  },
  props: {
    room: Object,
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