import Vue from 'vue'
import Vuex from 'vuex'
import justRestAPI from '@/store/justRestService.js'

Vue.use(Vuex);

export default new Vuex.Store({
  state: {
    rooms: {},
  },
  mutations: {
    setRooms (state, rooms) {
      for (var i = 0 ; i < rooms.length ; i++) {
        Vue.set(state.rooms, rooms[i].id, rooms[i])
      }
    },
    setScenario (state, {roomId, scenario}) {
      if (!state.rooms) {
        // eslint-disable-next-line
        console.error("No room to update")
        return
      }

      if (state.rooms[roomId] == undefined) {
        // eslint-disable-next-line
        console.error("Room not found")
      } else {
        state.rooms[roomId].scenario = scenario
      }
    },
    setCardinal (state, {roomId, cardinal}) {
      if (!state.rooms) {
        // eslint-disable-next-line
        console.error("No room to update")
        return
      }

      if (state.rooms[roomId] == undefined) {
        // eslint-disable-next-line
        console.error("Room not found")
      } else {
        state.rooms[roomId].cardinal = cardinal
      }
    },
    setChannel (state, {roomId, channel}) {
      if (!state.rooms) {
        // eslint-disable-next-line
        console.error("No room to update")
        return
      }

      if (state.rooms[roomId] == undefined) {
        // eslint-disable-next-line
        console.error("Room not found")
      } else {
        state.rooms[roomId].channel = channel
      }
    },
    setRoomLiveData (state, {roomId, liveData}) {
      if (!state.rooms) {
        // eslint-disable-next-line
        console.error("No room to update")
        return
      }

      if (state.rooms[roomId] == undefined) {
        // eslint-disable-next-line
        console.error("Room not found")
      } else {
        state.rooms[roomId].liveData = liveData
      }
    },
    setClock (state, {roomId, ticks}) {
      if (!state.rooms) {
        // eslint-disable-next-line
        console.error("No room to update")
        return
      }

      if (state.rooms[roomId] == undefined) {
        // eslint-disable-next-line
        console.error("Room not found")
      } else {
        state.rooms[roomId].liveData.ticks = ticks
      }
    },
    addRecord (state, {roomId, record}) {
      if (!state.rooms) {
        // eslint-disable-next-line
        console.error("No room to update")
        return
      }

      if (state.rooms[roomId] == undefined) {
        // eslint-disable-next-line
        console.error("Room not found")
      } else {
        state.rooms[roomId].liveData.records.push(record)
      }
    },
    processReset (state, roomId) {
      if (!state.rooms) {
        // eslint-disable-next-line
        console.error("No room to update")
        return
      }

      if (state.rooms[roomId] == undefined) {
        // eslint-disable-next-line
        console.error("Room not found")
      } else {
        state.rooms[roomId].liveData.ticks = 0
        state.rooms[roomId].liveData.records = []
      }
    },
    setCameras (state, {roomId, cameras}) {
      if (!state.rooms) {
        // eslint-disable-next-line
        console.error("No room to update")
        return
      }

      if (state.rooms[roomId] == undefined) {
        // eslint-disable-next-line
        console.error("Room not found")
      } else {
        state.rooms[roomId].cameras = cameras
      }
    },
    setCameraName (state, {roomId, cameraIndex, name}) {
      if (!state.rooms) {
        // eslint-disable-next-line
        console.error("No room to update")
        return
      }

      if (state.rooms[roomId] == undefined) {
        // eslint-disable-next-line
        console.error("Room not found")
        return
      }

      if (state.rooms[roomId].cameras == undefined) {
        // eslint-disable-next-line
        console.error("Cameras have not been fetched")
        return
      }

      if (state.rooms[roomId].cameras[cameraIndex] == undefined) {
        // eslint-disable-next-line
        console.error("Camera index " + cameraIndex + " does not exist")
        return
      }

      state.rooms[roomId].cameras[cameraIndex].name = name
    },
    setCameraURL (state, {roomId, cameraIndex, url}) {
      if (!state.rooms) {
        // eslint-disable-next-line
        console.error("No room to update")
        return
      }

      if (state.rooms[roomId] == undefined) {
        // eslint-disable-next-line
        console.error("Room not found")
        return
      }

      if (state.rooms[roomId].cameras == undefined) {
        // eslint-disable-next-line
        console.error("Cameras have not been fetched")
        return
      }

      if (state.rooms[roomId].cameras[cameraIndex] == undefined) {
        // eslint-disable-next-line
        console.error("Camera index " + cameraIndex + " does not exist")
        return
      }

      state.rooms[roomId].cameras[cameraIndex].url = url
    }
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
                    // eslint-disable-next-line
                    console.error(response.data.error)
                  }
                })
                .catch(function (error) {
                  // eslint-disable-next-line
                  console.error(error)
                })
            })
          } else {
            // eslint-disable-next-line
            console.error(response.data.error)
          }
        })
        .catch(function (error) {
          // eslint-disable-next-line
          console.error(error)
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
            // eslint-disable-next-line
            console.error(response.data.error)
          }
        })
        .catch(function (error) {
          // eslint-disable-next-line
          console.error(error)
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
    }
  }
})
