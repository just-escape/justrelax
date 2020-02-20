import Vue from 'vue'
import VueNativeSock from 'vue-native-websocket'
import BootstrapVue from 'bootstrap-vue'
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'

import justSockService from '@/store/justSockService.js'

import App from './App.vue'

Vue.use(VueNativeSock, 'ws://192.168.1.75:3031', {
  store: justSockService,
  connectManually: true,
  reconnection: true,
  reconnectionDelay: 10000,
})
Vue.use(BootstrapVue)

Vue.config.productionTip = false

new Vue({
  render: h => h(App),
}).$mount('#app')
