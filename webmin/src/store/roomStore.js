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
  },
  actions: {
    fetchRooms() {
      publishSubscribeService.commit('subscribe', 'd1.webmin')
      publishSubscribeService.commit('subscribe', 'd2.webmin')
      publishSubscribeService.commit('subscribe', 'justescape.webmin')
      publishSubscribeService.commit('addOnConnectionPublication', {channel: 'd1.scenario', event: {'category': 'request_session_data_for_webmin'}})
      publishSubscribeService.commit('addOnConnectionPublication', {channel: 'd2.scenario', event: {'category': 'request_session_data_for_webmin'}})
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
