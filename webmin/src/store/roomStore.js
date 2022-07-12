import Vue from 'vue'
import Vuex from 'vuex'
import publishSubscribeService from '@/store/publishSubscribeService.js'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    rooms: [
      {
        id: 1,
        name: 'Digimiam zone 1',
        toolbar: 'digimiam',
        default_publication_channel: 'd1.scenario',
        subscription_channels: ['d1.webmin'],
      },
      {
        id: 2,
        name: 'Digimiam zone 2',
        toolbar: 'digimiam',
        default_publication_channel: 'd2.scenario',
        subscription_channels: ['d2.webmin'],
      },
      {
        id: 3,
        name: 'Just Escape',
        default_publication_channel: 'justescape',
        subscription_channels: ['justescape.webmin'],
      },
    ],
    sessionData: {1: {}, 2: {}, 3: {}},
  },
  mutations: {
    /*setRooms (state, rooms) {
      state.sessionData = {}  // Reset
      for (var room of rooms) {
        state.sessionData[room.id] = {}
        room.default_publication_channel = 'd1.scenario'
        room.subscribed_channels = ['d1.webmin']
      }
      Vue.set(state, 'rooms', rooms)
    },*/
    setRoomDefaultPublicationChannel(state, {roomId, defaultPublicationChannel}) {
      for (var room of state.rooms) {
        if (room.id == roomId) {
          room.default_publication_channel = defaultPublicationChannel
        }
      }
    },
    processEvent(state, {channel, event}) {
      for (var room of state.rooms) {
        if (room.subscription_channels.includes(channel)) {
          if (event.category === 'set_session_data') {
            Vue.set(state.sessionData[room.id], event.key, event.data)
          }
        }
      }
    },
    /*setCameras (state, {roomId, cameras}) {
      for (var room of state.rooms) {
        if (room.id === roomId) {
          Vue.set(room, 'cameras', cameras)
        }
      }
    },
    setCards (state, {roomId, cards}) {
      for (var room of state.rooms) {
        if (room.id === roomId) {
          Vue.set(room, 'cards', cards)
        }
      }
    },
    setCardRows (state, {roomId, cardId, cardRows}) {
      for (var room of state.rooms) {
        if (room.id === roomId) {
          for (var card of room.cards) {
            if (card.id === cardId) {
              Vue.set(card, 'rows', cardRows)
            }
          }
        }
      }
    },
    /* setRuleSets (state, ruleSets) {
      state.ruleSets = ruleSets
    },*/
  },
  actions: {
    /*fetchScenarios (context) {
      Vue.prototype.$justRestAPI.get('/scenario/')
        .then(function (response) {
          var scenarios = response.data
          context.dispatch('fetchRooms', scenarios[0].id)
        })
        .catch(function (error) {
          notificationStore.dispatch('pushError', 'Error while fetching scenarios: ' + error)
        })
    },
    fetchRuleSets (context) {
      Vue.prototype.$justRestAPI.get('/rule_set/')
        .then(response => {
          var ruleSets = response.data
          context.commit('setRuleSets', ruleSets)
        })
        .catch(error => {
          notificationStore.dispatch('pushError', 'Error while fetching rule sets: ' + error)
        })
    },*/
    fetchRooms() {
      publishSubscribeService.commit('subscribe', 'd1.webmin')
      publishSubscribeService.commit('subscribe', 'd2.webmin')
      publishSubscribeService.commit('subscribe', 'justescape.webmin')
      publishSubscribeService.commit('addOnConnectionPublication', {channel: 'd1.scenario', event: {'category': 'request_session_data_for_webmin'}})
      publishSubscribeService.commit('addOnConnectionPublication', {channel: 'd2.scenario', event: {'category': 'request_session_data_for_webmin'}})

      /*for (var room of rooms) {
        for (var channel of room.subscription_channels) {
          publishSubscribeService.commit('subscribe', channel)
        }
      }*/
      /*Vue.prototype.$justRestAPI.get('/room')
        .then(function (response) {
          var rooms = response.data
          for (var room of rooms) {
            room.scenario = "Le digimiam"
          }
          roomStore.commit('setRooms', rooms)
          for (var room of rooms) {
            publishSubscribeService.commit('subscribe', room.channel)
          }
        })
        .catch(function (error) {
          notificationStore.dispatch('pushError', 'Error while fetching rooms: ' + error)
        })*/
    },
    widgetAction (context, {channel, widgetId, widgetType, ...extra}) {
      let event = {
        category: "webmin_widget_action",
        widget_id: widgetId,
        widget_type: widgetType,
        ...extra,
      }
      publishSubscribeService.commit('publish', {channel: channel, event: event})
    },
  },
})
