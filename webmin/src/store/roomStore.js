import Vue from 'vue'
import Vuex from 'vuex'
import justRestAPI from '@/store/justRestService.js'

Vue.use(Vuex);

export default new Vuex.Store({
  state: {
    rooms: null,
  },
  mutations: {
    setRooms (state, rooms) {
      state.rooms = rooms
    },
    setClock (state, {channel, ticks}) {
      if (!state.rooms) {
        // eslint-disable-next-line
        console.error("No room to update")
        return
      }

      for (var i = 0 ; i < state.rooms.length ; i++) {
        if (state.rooms[i].channel == channel) {
          state.rooms[i].ticks = ticks
        }
      }
    },
    addRecord (state, {channel, record}) {
      if (!state.rooms) {
        // eslint-disable-next-line
        console.error("No room to add record to")
        return
      }

      for (var i = 0 ; i < state.rooms.length ; i++) {
        if (state.rooms[i].channel == channel) {
          state.rooms[i].records.push(record)
        }
      }
    },
    processReset (state, channel) {
      if (!state.rooms) {
        // eslint-disable-next-line
        console.error("No room to add record to")
        return
      }
      for (var i = 0 ; i < state.rooms.length ; i++) {
        if (state.rooms[i].channel == channel) {
          state.rooms[i].records = []
          state.rooms[i].ticks = 0
        }
      }
    }
  },
  actions: {
    fetchRooms (context) {
      var rooms = []
      justRestAPI.get('/get_rooms')
        .then(function (response) {
          if (response.data.success) {
            rooms = response.data.content
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
    runRoom (context, channel) {
      var formData = new FormData()
      formData.append('channel', channel)
      justRestAPI.post('/run_room', formData)
    },
    haltRoom (context, channel) {
      var formData = new FormData()
      formData.append('channel', channel)
      justRestAPI.post('/halt_room', formData)
    },
    resetRoom (context, channel) {
      var formData = new FormData()
      formData.append('channel', channel)
      justRestAPI.post('/reset_room', formData)
    },
    beat(context, {channel, ticks}) {
      context.commit('setClock', {channel, ticks})
    },
    addRecord(context, {channel, record}) {
      context.commit('addRecord', {channel, record})
    },
    processReset(context, channel) {
      context.commit('processReset', channel)
    },
    processAction(context, {channel, action}) {
      var formData = new FormData()
      formData.append('channel', channel)
      formData.append('name', action)
      justRestAPI.post('/process_action', formData)
    }
  }
})
