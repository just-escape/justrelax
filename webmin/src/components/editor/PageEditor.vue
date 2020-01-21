<template>
  <AppContent>
    <AppContentTitle class="d-flex flex-row" slot="header-left">
      <AppContentTitle class="mr-5">
        Editor
      </AppContentTitle>
      <b-button-group class="my-auto">
        <ButtonJaffa @click="save()">
          <i class="far fa-save fa-lg"></i>
        </ButtonJaffa>
      </b-button-group>
    </AppContentTitle>
    <div slot="main" v-if="!room">
      Room not found
    </div>
    <div slot="main" class="mt-2 h-100" v-else>
      <Rules/>
    </div>
  </AppContent>
</template>

<script>
import ButtonJaffa from '@/components/common/ButtonJaffa.vue'
import AppContent from '@/components/common/AppContent.vue'
import AppContentTitle from '@/components/common/AppContentTitle.vue'
import Rules from '@/components/editor/Rules.vue'
import roomStore from '@/store/roomStore.js'
import editorStore from '@/store/editorStore.js'

export default {
  name: 'PageEditor',
  components: {
    ButtonJaffa,
    AppContent,
    AppContentTitle,
    Rules,
  },
  data() {
    return {
      rules: '',
    }
  },
  computed: {
    room() {
      return roomStore.getters.room(this.roomId)
    },
  },
  methods: {
    loadEditorData() {
      editorStore.dispatch('loadEditorData')
    },
    save() {
      editorStore.dispatch('save')
    },
  },
  created() {
    this.loadEditorData()
  },
  props: ['roomId']
}
</script>
