<template>
  <div>
    <div class="d-flex flex-row justify-content-between p-3">
      <div>
        <a :href="'/rooms/' + room.id + '/live'">
          <i class="text-jaffa fas fa-door-open fa-fw fa-lg mr-3"></i>{{ room.name }}
        </a>
      </div>
      <div class="d-flex flex-row">
        <Clock class="mr-2" :roomId="room.id" :data="'gameTime'" :displayZero="true"/>
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
import Clock from '@/components/common/Clock.vue'

export default {
  name: 'TabRoom',
  components: {
    CollapseChevron,
    Clock,
    Tab,
  },
  computed: {
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