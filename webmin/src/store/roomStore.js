import Vue from 'vue'
import Vuex from 'vuex'
import publishSubscribeService from '@/store/publishSubscribeService.js'
// import notificationStore from '@/store/notificationStore.js'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    rooms: [
      {
        id: 1,
        name: 'Digimiam zone 1',
        default_publication_channel: 'd1.scenario',
        subscription_channels: ['d1.webmin'],
      },
      {
        id: 2,
        name: 'Digimiam zone 2',
        default_publication_channel: 'd2.scenario',
        subscription_channels: ['d2.webmin'],
      },
    ],
    sessionData: {1: {}, 2: {}},
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
    processEvent(state, {channel, event}) {
      for (var room of state.rooms) {
        if (room.subscription_channels.contains(channel)) {
          if (event.category === 'set_session_data') {
            state.sessionData[room.id][event.key] = event.data
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
