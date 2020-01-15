import Vue from 'vue'
import Vuex from 'vuex'
import axios from 'axios'

Vue.use(Vuex);

const justRestAPI = axios.create({
  baseURL: 'http://localhost:8000'
})

export default justRestAPI
