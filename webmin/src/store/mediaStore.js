import moment from 'moment'
import Vue from 'vue'
import Vuex from 'vuex'
import justRestAPI from '@/store/justRestService.js'
import notificationStore from '@/store/notificationStore.js'

Vue.use(Vuex);

export default new Vuex.Store({
  state: {
    medias: null,
  },
  mutations: {
    setMedias (state, medias) {
      state.medias = medias
    },
  },
  actions: {
    fetchMedias (context) {
      var medias = []
      justRestAPI.get('/medias')
        .then(function (response) {
          if (response.data.success) {
            medias = response.data.content
            medias.map(function (media) {
              media.date = moment.unix(media.date).format('MM/DD/YYYY')
            })
          } else {
            notificationStore.dispatch('displayNotification', 'Error while fetching medias: ' + response.data.error)
          }
        })
        .catch(function (error) {
          notificationStore.dispatch('displayNotification', 'Error while fetching medias: ' + error)
        })
        .finally(function () {
          context.commit('setMedias', medias)
        })
    },
  }
})
