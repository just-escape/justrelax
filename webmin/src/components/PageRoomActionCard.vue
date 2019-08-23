<template>
  <b-card
    :header="header"
    header-tag="h3"
    header-class="big-noodle text-jaffa text-center"
    class="bgc-dark border-jaffa h-100"
  >
    <ul class="list-unstyled mb-0">
      <li
        v-for="(subcategory, index) in subcategories"
        :key="subcategory.id"
        :class="getSubcategoryClasses(index)"
      >
        <div>
          {{ subcategory.name }}
        </div>
        <b-button-group>
          <ButtonJaffa
            size="sm"
            v-for="action in subcategory.actions"
            :key="action.id"
            @click="processAction(action.name)"
          >
            <i :class="action.icon"></i>
          </ButtonJaffa>
        </b-button-group>
      </li>
    </ul>
  </b-card>
</template>

<script>
import ButtonJaffa from '@/components/ButtonJaffa.vue'
import roomStore from '@/store/roomStore.js'

export default {
  name: 'PageRoomActionCard',
  components: {
    ButtonJaffa
  },
  computed: {
    lastSubcategoryIndex() {
      return Object.keys(this.subcategories).length - 1;
    }
  },
  methods: {
    getSubcategoryClasses(index) {
      var classes = 'd-flex justify-content-between align-items-center'
      if (index != this.lastSubcategoryIndex) {
        classes = classes + ' mb-2'
      }
      return classes
    },
    processAction (action) {
      var roomId = this.roomId
      roomStore.dispatch('processAction', {roomId, action})
    }
  },
  props: [
    'roomId',
    'header',
    'subcategories',
  ]
}
</script>
