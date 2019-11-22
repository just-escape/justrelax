import Vue from 'vue'
import Vuex from 'vuex'
import justRestAPI from '@/store/justRestService.js'
import notificationStore from '@/store/notificationStore.js'

Vue.use(Vuex);

export default new Vuex.Store({
  state: {
    rooms: {},
  },
  getters: {
    room (state) {
      return function (roomId) {
        var parsedRoomId = parseInt(roomId, 10)
        if (Number.isNaN(parsedRoomId)) {
          return null
        }

        if (state.rooms && state.rooms[parsedRoomId] != undefined) {
          return state.rooms[parsedRoomId]
        } else {
          return null
        }
      }
    }
  },
  mutations: {
    setRooms (state, rooms) {
      for (var i = 0 ; i < rooms.length ; i++) {
        Vue.set(state.rooms, rooms[i].id, rooms[i])
      }
    },
    setScenario (state, {roomId, scenario}) {
      if (!state.rooms) {
        notificationStore.dispatch('pushError', 'No rooms to set scenario')
        return
      }

      if (state.rooms[roomId] == undefined) {
        notificationStore.dispatch('pushError', 'Room id=' + roomId + ' not found to set scenario')
      } else {
        state.rooms[roomId].scenario = scenario
      }
    },
    setCardinal (state, {roomId, cardinal}) {
      if (!state.rooms) {
        notificationStore.dispatch('pushError', 'No rooms to set cardinal')
        return
      }

      if (state.rooms[roomId] == undefined) {
        notificationStore.dispatch('pushError', 'Room id=' + roomId + ' not found to set cardinal')
      } else {
        state.rooms[roomId].cardinal = cardinal
      }
    },
    setChannel (state, {roomId, channel}) {
      if (!state.rooms) {
        notificationStore.dispatch('pushError', 'No rooms to set channel')
        return
      }

      if (state.rooms[roomId] == undefined) {
        notificationStore.dispatch('pushError', 'Room id=' + roomId + ' not found to set channel')
      } else {
        state.rooms[roomId].channel = channel
      }
    },
    setRoomLiveData (state, {roomId, liveData}) {
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
    setClock (state, {roomId, ticks}) {
      if (!state.rooms) {
        notificationStore.dispatch('pushError', 'No rooms to set clock')
        return
      }

      if (state.rooms[roomId] == undefined) {
        notificationStore.dispatch('pushError', 'Room id=' + roomId + ' not found to set clock')
      } else {
        state.rooms[roomId].liveData.ticks = ticks
      }
    },
    addRecord (state, {roomId, record}) {
      if (!state.rooms) {
        notificationStore.dispatch('pushError', 'No rooms to add record')
        return
      }

      if (state.rooms[roomId] == undefined) {
        notificationStore.dispatch('pushError', 'Room id=' + roomId + ' not found to add record')
      } else {
        state.rooms[roomId].liveData.records.push(record)
      }
    },
    processReset (state, roomId) {
      if (!state.rooms) {
        notificationStore.dispatch('pushError', 'No rooms to process reset')
        return
      }

      if (state.rooms[roomId] == undefined) {
        notificationStore.dispatch('pushError', 'Room id=' + roomId + ' not found to process reset')
      } else {
        state.rooms[roomId].liveData.ticks = 0
        state.rooms[roomId].liveData.records = []
      }
    },
    setCameras (state, {roomId, cameras}) {
      if (!state.rooms) {
        notificationStore.dispatch('pushError', 'No room to set cameras')
        return
      }

      if (state.rooms[roomId] == undefined) {
        notificationStore.dispatch('pushError', 'Room id=' + roomId + ' not found to set cameras')
      } else {
        state.rooms[roomId].cameras = cameras
      }
    },
    setCameraName (state, {roomId, cameraIndex, name}) {
      if (!state.rooms) {
        notificationStore.dispatch('pushError', 'No rooms to set camera name')
        return
      }

      if (state.rooms[roomId] == undefined) {
        notificationStore.dispatch('pushError', 'Room id=' + roomId + ' not found to set camera name')
        return
      }

      if (state.rooms[roomId].cameras == undefined) {
        notificationStore.dispatch('pushError', 'Room id=' + roomId + ' has no cameras to set name')
        return
      }

      if (state.rooms[roomId].cameras[cameraIndex] == undefined) {
        notificationStore.dispatch('pushError', 'Room id=' + roomId + ' has no camera id=' + cameraIndex + ' to set name')
        return
      }

      state.rooms[roomId].cameras[cameraIndex].name = name
    },
    setCameraURL (state, {roomId, cameraIndex, url}) {
      if (!state.rooms) {
        notificationStore.dispatch('pushError', 'No rooms to set camera URL')
        return
      }

      if (state.rooms[roomId] == undefined) {
        notificationStore.dispatch('pushError', 'Room id=' + roomId + ' not found to set camera URL')
        return
      }

      if (state.rooms[roomId].cameras == undefined) {
        notificationStore.dispatch('pushError', 'Room id=' + roomId + ' has no cameras to set URL')
        return
      }

      if (state.rooms[roomId].cameras[cameraIndex] == undefined) {
        notificationStore.dispatch('pushError', 'Room id=' + roomId + ' has no camera id=' + cameraIndex + ' to set URL')
        return
      }

      state.rooms[roomId].cameras[cameraIndex].url = url
    },
  },
  actions: {
    fetchRooms (context) {
      var rooms = []
      justRestAPI.get('/rooms')
        .then(function (response) {
          if (response.data.success) {
            rooms = response.data.content
            rooms.map(function(room) {
              room.cameras = undefined
              room.liveData = {"ticks": 0, "records": []}
              justRestAPI.get('/rooms/' + room.id + '/get_live_data')
                .then(function (response) {
                  if (response.data.success) {
                    var roomId = room.id
                    var liveData = response.data.content
                    context.commit('setRoomLiveData', {roomId, liveData})
                  } else {
                    notificationStore.dispatch('pushError', 'Error while fetching room live data: ' + response.data.error)
                  }
                })
                .catch(function (error) {
                  notificationStore.dispatch('pushError', 'Error while fetching room live data: ' + error)
                })
            })
          } else {
            notificationStore.dispatch('pushError', 'Error while fetching rooms: ' + response.data.error)
          }
        })
        .catch(function (error) {
          notificationStore.dispatch('pushError', 'Error while fetching rooms: ' + error)
        })
        .finally(function () {
          context.commit('setRooms', rooms)
        })
    },
    fetchCameras (context, roomId) {
      var cameras = []
      justRestAPI.get('/rooms/' + roomId + '/cameras')
        .then(function (response) {
          if (response.data.success) {
            cameras = response.data.content
          } else {
            notificationStore.dispatch('pushError', 'Error while fetching cameras: ' + response.data.error)
          }
        })
        .catch(function (error) {
          notificationStore.dispatch('pushError', 'Error while fetching cameras: ' + error)
        })
        .finally(function () {
          context.commit('setCameras', {roomId, cameras})
        })
    },
    runRoom (context, roomId) {
      var formData = new FormData()
      formData.append('n_players', 0)
      justRestAPI.post('/rooms/' + roomId + '/run', formData)
    },
    haltRoom (context, roomId) {
      justRestAPI.post('/rooms/' + roomId + '/halt')
    },
    resetRoom (context, roomId) {
      justRestAPI.post('/rooms/' + roomId + '/reset')
    },
    updateRules (context, {roomId, rules}) {
      var formData = new FormData()
      formData.append('rules', rules)
      justRestAPI.post('/rooms/' + roomId + '/rules', formData)
        .then(function (response) {
          if (response.data.success) {
            notificationStore.dispatch('pushNotification', 'Rules updated with success')
          } else {
            notificationStore.dispatch('pushError', 'Error while updating rules: ' + response.data.error)
          }
        })
        .catch(function (error) {
          notificationStore.dispatch('pushError', 'Error while updating rules: ' + error)
        })
    },
    beat(context, {roomId, ticks}) {
      context.commit('setClock', {roomId, ticks})
    },
    addRecord(context, {roomId, record}) {
      context.commit('addRecord', {roomId, record})
    },
    processReset(context, roomId) {
      context.commit('processReset', roomId)
    },
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
    },
  },
})
