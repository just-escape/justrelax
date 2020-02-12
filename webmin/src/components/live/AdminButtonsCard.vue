<template>
  <b-card
    :header="header"
    header-tag="h3"
    header-class="big-noodle text-jaffa text-center"
    class="bgc-dark border-jaffa h-100"
  >
    <ul class="list-unstyled mb-0">
      <li
        v-for="(row, rowIndex) in rows"
        :key="rowIndex"
        :class="getRowClasses(rowIndex)"
      >
        <div>
          {{ row.name }}
        </div>
        <b-button-group>
          <ButtonJaffa
            size="sm"
            v-for="button in row.buttons"
            :key="button.id"
            :id="'admin-button-' + cardIndex + '-' + rowIndex + '-' + button.id"
            @click="press(button.id)"
          >
            <i :class="button.icon"></i>
            <b-popover
              :target="'admin-button-' + cardIndex + '-' + rowIndex + '-' + button.id"
              triggers=""
              disabled
              :show="showButtonIds"
              placement="top"
            >
              {{ button.id }}
            </b-popover>
          </ButtonJaffa>
        </b-button-group>
      </li>
    </ul>
  </b-card>
</template>

<script>
import ButtonJaffa from '@/components/common/ButtonJaffa.vue'
import roomStore from '@/store/roomStore.js'

export default {
  name: 'AdminButtonsCard',
  components: {
    ButtonJaffa
  },
  computed: {
    lastRowIndex() {
      return Object.keys(this.rows).length - 1;
    }
  },
  methods: {
    getRowClasses(index) {
      var classes = 'd-flex justify-content-between align-items-center'
      if (index != this.lastRowIndex) {
        classes = classes + ' mb-2'
      }
      return classes
    },
    press (buttonId) {
      let roomId = this.roomId
      roomStore.dispatch('pressedAdminButton', {roomId, buttonId})
    }
  },
  props: {
    roomId: {
      type: Number,
      mandatory: true,
    },
    header: {
      type: String,
      mandatory: true,
    },
    rows: {
      type: Array,
      mandatory: true,
    },
    cardIndex: {
      type: Number,
      mandatory: true,
    },
    showButtonIds: {
      type: Boolean,
      default: false,
    },
  }
}
</script>
