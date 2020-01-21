import Vue from 'vue'
import Vuex from 'vuex'
import justSockService from '@/store/justSockService.js'
import justRestAPI from '@/store/justRestService.js'
import notificationStore from '@/store/notificationStore.js'

Vue.use(Vuex);

export default new Vuex.Store({
  state: {
    rooms: [],
  },
  getters: {
    room (state) {
      return function (roomId) {
        var parsedRoomId = parseInt(roomId, 10)
        if (Number.isNaN(parsedRoomId)) {
          return null
        }

        for (var room of state.rooms) {
          if (room.id === parsedRoomId) {
            return room
          }
        }

        return null
      }
    }
  },
  mutations: {
    addRooms (state, rooms) {
      for (var room of rooms) {
        room.liveData = {
          ticks: 0,
          records: [],
        }
      }
      Vue.set(state, 'rooms', rooms)
    },
    /*setRoomLiveData (state, {roomId, liveData}) {
      if (!state.rooms) {
        notificationStore.dispatch('pushError', 'No rooms to set live data')
        return
      }

      if (state.rooms[roomId] == undefined) {
        notificationStore.dispatch('pushError', 'Room id=' + roomId + ' not found to set live data')
      } else {
        state.rooms[roomId].liveData = liveData
      }
    },
    addRecord (state, {roomId, recordId, recordTicks, recordLabel}) {
      if (!state.rooms) {
        notificationStore.dispatch('pushError', 'No rooms to add record')
        return
      }

      if (state.rooms[roomId] == undefined) {
        notificationStore.dispatch('pushError', 'Room id=' + roomId + ' not found to add record')
      } else {
        state.rooms[roomId].liveData.records.push(record)
      }
    },*/
    setClock (state, {roomId, ticks}) {
      for (var room of state.rooms) {
        if (room.id === roomId) {
          room.liveData.ticks = ticks
        }
      }
    },
    processReset (state, roomId) {
      for (var room of state.rooms) {
        if (room.id === roomId) {
          room.liveData.ticks = 0
          room.liveData.records = []
        }
      }
    },
    setCameras (state, {roomId, cameras}) {
      for (var room of state.rooms) {
        if (room.id === roomId) {
          Vue.set(room, 'cameras', cameras)
        }
      }
    },
  },
  actions: {
    fetchScenarios (context) {
      justRestAPI.get('/scenario/')
        .then(function (response) {
          var scenarios = response.data
          context.dispatch('fetchRooms', scenarios[0].id)
        })
        .catch(function (error) {
          notificationStore.dispatch('pushError', 'Error while fetching scenarios: ' + error)
        })
    },
    fetchRooms (context, scenarioId) {
      justRestAPI.get('/room/?scenario=' + scenarioId)
        .then(function (response) {
          var rooms = response.data
          for (var room of rooms) {
            room.scenario = "Le digimiam"
          }
          rooms.cameras = []
          context.commit('addRooms', rooms)
        })
        .catch(function (error) {
          notificationStore.dispatch('pushError', 'Error while fetching rooms: ' + error)
        })
    },
    fetchCameras (context, roomId) {
      justRestAPI.get('/camera/?room=' + roomId)
        .then(function (response) {
          let cameras = response.data
          context.commit('setCameras', {roomId, cameras})
        })
        .catch(function (error) {
          notificationStore.dispatch('pushError', 'Error while fetching cameras: ' + error)
        })
    },
    beat(context, {roomId, ticks}) {
      context.commit('setClock', {roomId, ticks})
    },
    addRecord(context, {roomId, record}) {
      context.commit('addRecord', {roomId, record})
    },
    runRoom (context, roomId) {
      let message = {
        room_id: roomId,
        message_type: "RUN",
      }
      justSockService.commit('sendMessage', message)
    },
    haltRoom (context, roomId) {
      let message = {
        room_id: roomId,
        message_type: "HALT",
      }
      justSockService.commit('sendMessage', message)
    },
    resetRoom (context, roomId) {
      let message = {
        room_id: roomId,
        message_type: "RESET",
      }
      justSockService.commit('sendMessage', message)
    },
    /*
    processAction(context, {roomId, action}) {
      var formData = new FormData()
      formData.append('name', action)
      justRestAPI.post('/rooms/' + roomId + '/action', formData)
        .then(function (response) {
          if (!response.data.success) {
            notificationStore.dispatch('pushError', 'Error while processing action: ' + response.data.error)
          }
        })
        .catch(function (error) {
          notificationStore.dispatch('pushError', 'Error while processing action: ' + error)
        })
    },
    processSendMessage(context, {roomId, to, content, json}) {
      let formData = new FormData()
      formData.append('to', to)
      formData.append('content', content)
      formData.append('json', json)
      justRestAPI.post('/rooms/' + roomId + '/send_message', formData)
      .then(function (response) {
        if (!response.data.success) {
          notificationStore.dispatch('pushError', 'Error while sending message: ' + response.data.error)
        }
      })
      .catch(function (error) {
        notificationStore.dispatch('pushError', 'Error while sending message: ' + error)
      })
    },*/
  },
})
