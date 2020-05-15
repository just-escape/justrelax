import Vue from 'vue'
import VueNativeSock from 'vue-native-websocket'
import BootstrapVue from 'bootstrap-vue'
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'

import justSockService from '@/store/justSockService.js'

import router from '@/router.js'
import i18n from '@/locales.js'

import App from './App.vue'

Vue.use(VueNativeSock, 'ws://localhost:3031', {
  store: justSockService,
  connectManually: true,
  reconnection: true,
  reconnectionDelay: 10000,
})
Vue.use(BootstrapVue)

Vue.config.productionTip = false

new Vue({
  render: h => h(App),
  router: router,
  i18n: i18n,
}).$mount('#app')
