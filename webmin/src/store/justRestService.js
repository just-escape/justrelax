import Vue from 'vue'
import Vuex from 'vuex'
import axios from 'axios'

Vue.use(Vuex);

const justRestAPI = axios.create({
  baseURL: 'http://localhost:3032'
})

export default justRestAPI