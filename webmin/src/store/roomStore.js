import Vue from 'vue'
import Vuex from 'vuex'
import justSockService from '@/store/justSockService.js'
import justRestAPI from '@/store/justRestService.js'
import notificationStore from '@/store/notificationStore.js'

Vue.use(Vuex);

export default new Vuex.Store({
  state: {
    rooms: [],
    onHoldLiveData: {},
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
        if (state.onHoldLiveData[room.id] !== undefined) {
          room.liveData = JSON.parse(JSON.stringify(state.onHoldLiveData[room.id]))
          delete state.onHoldLiveData[room.id]
        } else {
          room.liveData = {
            sessionTime: 0,
            records: [],
          }
        }
      }
      Vue.set(state, 'rooms', rooms)
    },
    pushLiveData (state, {roomId, sessionTime, records}) {
      /* Receiving rooms or live data first is not deterministic. If a room if found, the live data is set.
       * Otherwise, the live data is put on hold until a room with the same id is received from the REST API.
       **/
      var foundARoom = false
      for (var room of state.rooms) {
        if (room.id === roomId) {
          foundARoom = true
          room.liveData.sessionTime = sessionTime
          room.liveData.records = records
        }
      }

      if (foundARoom === false) {
        state.onHoldLiveData[roomId] = {
          sessionTime: sessionTime,
          records: records,
        }
      }
    },
    addRecord (state, {roomId, recordId, recordSessionTime, recordLabel}) {
      for (var room of state.rooms) {
        if (room.id === roomId) {
          room.liveData.records.push(
            {
              id: recordId,
              session_time: recordSessionTime,
              label: recordLabel,
            }
          )
        }
      }
    },
    setClock (state, {roomId, sessionTime}) {
      for (var room of state.rooms) {
        if (room.id === roomId) {
          room.liveData.sessionTime = sessionTime
        }
      }
    },
    processReset (state, roomId) {
      for (var room of state.rooms) {
        if (room.id === roomId) {
          room.liveData.sessionTime = 0
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
    ticTac(context, {roomId, sessionTime}) {
      context.commit('setClock', {roomId, sessionTime})
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
    processSendEventTo(context, {roomId, node, event}) {
      let message = {
        room_id: roomId,
        message_type: "SEND_EVENT_TO",
        node: node,
        event: event,
      }
      justSockService.commit('sendMessage', message)
    },
    processSendEventAs(context, {roomId, node, event}) {
      let message = {
        room_id: roomId,
        message_type: "SEND_EVENT_AS",
        node: node,
        event: event,
      }
      justSockService.commit('sendMessage', message)
    },
  },
})
