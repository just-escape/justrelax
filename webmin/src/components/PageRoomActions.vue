<template>
  <div>
    <h2 class="big-noodle text-jaffa text-center">Actions</h2>
    <div class="row">
      <div
        v-for="category in room.rules.admin.categories"
        :key="category.id"
        class="col-3"
      >
        <PageRoomActionCard
          :roomId="room.id"
          :header="category.name"
          :subcategories="category.subcategories"
        />
      </div>
    </div>
  </div>
</template>

<script>
import PageRoomActionCard from '@/components/PageRoomActionCard.vue'

export default {
  name: 'PageRoomActions',
  components: {
    PageRoomActionCard
  },
  props: ['room']
}
</script>
