<template>
  <div>
    <h2 class="big-noodle text-jaffa text-center">
      <span class="mr-3">{{ $t('admin_buttons') }}</span>
      <ButtonJaffa
        size="sm"
        @click="showButtonIds = !showButtonIds"
      >
        <i class="far fa-comment-alt"></i>
      </ButtonJaffa>
    </h2>
    <div class="row">
      <div
        v-for="(card, index) in buttonCards"
        :key="card.name"
        class="col-3 mb-4"
      >
        <AdminButtonsCard
          :roomId="room.id"
          :header="card.name"
          :rows="card.rows"
          :cardIndex="index"
          :showButtonIds="showButtonIds"
        />
      </div>
    </div>
  </div>
</template>

<script>
import ButtonJaffa from '@/components/common/ButtonJaffa.vue'
import AdminButtonsCard from '@/components/live/AdminButtonsCard.vue'

export default {
  name: 'AdminButtons',
  components: {
    AdminButtonsCard,
    ButtonJaffa,
  },
  data() {
    return {
      showButtonIds: false,
    }
  },
  props: {
    buttonCards: {
      type: Array,
      mandatory: true,
    },
    room: {
      type: Object,
      mandatory: true,
    },
  }
}
</script>
