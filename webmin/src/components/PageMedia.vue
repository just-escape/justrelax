<template>
  <AppContent>
    <AppContentTitle slot="header-left">
      Medias
    </AppContentTitle>
    <div slot="main">
      <h2 class="big-noodle text-jaffa">Files</h2>
      
      <b-form class="row mb-3">
        <div class="align-items-center d-flex col-1">
          <label for="filename" class="mb-0">New file</label>
        </div>
        <div class="col-3">
          <b-form-input
            id="filename"
            v-model="filename"
            required
            placeholder="theme.wav"
          ></b-form-input>
        </div>
        <div class="col-3">
          <b-form-file v-model="file"></b-form-file>
        </div>
        <div class="col-1">
          <ButtonJaffa type="submit" class="btn btn-block">Add</ButtonJaffa>
        </div>
      </b-form>

      <b-table
        v-if="displayMedias"
        striped
        small
        borderless
        :items="items"
        :fields="fields"
      >
        <template slot=" ">
          <div class="float-right">
            <i class="fas fa-download mr-2"></i>
            <i class="fas fa-volume-up mr-2"></i>
            <i class="fa fa-times mr-1"></i>
          </div>
        </template>
      </b-table>
      <div v-else>
        Fetching...
      </div>
    </div>
  </AppContent>
</template>

<script>
import AppContent from '@/components/AppContent.vue'
import AppContentTitle from '@/components/AppContentTitle.vue'
import ButtonJaffa from '@/components/ButtonJaffa.vue'
import mediaStore from '@/store/mediaStore.js'

export default {
  name: 'PageMedia',
  components: {
    AppContent,
    AppContentTitle,
    ButtonJaffa,
  },
  data: function() {
    return {
      fields: ['name', 'size', 'date', ' '],
      theme: '',
      filename: '',
      file: null,
    }
  },
  computed: {
    items: function() {
      return mediaStore.state.medias
    },
    displayMedias: function() {
      return this.items != undefined
    },
  },
  mounted() {
    mediaStore.dispatch('fetchMedias')
  },
}
</script>

<style scoped>
.form-control-file {
  width: auto;
}
</style>
