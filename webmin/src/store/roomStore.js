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
    setRoomLiveData (state, {roomId, liveData}) {
      if (!state.rooms) {
        // eslint-disable-next-line
        console.error("No room to update")
        return
      }

      if (state.rooms[roomId] == undefined) {
        // eslint-disable-next-line
        console.error("Room not found here")
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
        console.error("No room to add record to")
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
        console.error("No room to add record to")
        return
      }

      if (state.rooms[roomId] == undefined) {
        // eslint-disable-next-line
        console.error("Room not found")
      } else {
        state.rooms[roomId].liveData.ticks = 0
        state.rooms[roomId].liveData.records = []
      }
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
