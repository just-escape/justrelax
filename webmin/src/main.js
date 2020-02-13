import Vue from 'vue'
import axios from 'axios'
import VueAxios from 'vue-axios'
import VueNativeSock from 'vue-native-websocket'
import VueAnime from 'vue-animejs'
import BootstrapVue from 'bootstrap-vue'
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'

import justSockService from '@/store/justSockService.js'
import router from '@/router/index.js'
import i18n from '@/i18n.js'

import App from '@/App.vue'

Vue.use(VueAxios, axios)
Vue.use(VueNativeSock, 'ws://localhost:3031', {
  store: justSockService,
  connectManually: true,
  reconnection: true,
  reconnectionDelay: 10000,
})
Vue.use(VueAnime)
Vue.use(BootstrapVue)

Vue.config.productionTip = false

new Vue({
  render: h => h(App),
  router: router,
  i18n: i18n,
}).$mount('#app')
