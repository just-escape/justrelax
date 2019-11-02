import Vue from 'vue'
import Vue2TouchEvents from 'vue2-touch-events'
import VueNativeSock from 'vue-native-websocket'
import VueAnime from 'vue-animejs'
import BootstrapVue from 'bootstrap-vue'
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'

import justSockService from '@/store/justSockService.js'

import router from '@/router.js'
import i18n from '@/locales.js'

import App from '@/App.vue'

Vue.use(Vue2TouchEvents)

Vue.use(VueNativeSock, 'ws://localhost:3031', {
  store: justSockService,
  connectManually: true,
  reconnection: true,
  reconnectionDelay: 10000,
})

const moment = require('moment')
require('moment/locale/fr')
Vue.use(require('vue-moment'), {moment})

Vue.use(VueAnime)
Vue.use(BootstrapVue)

Vue.config.productionTip = false

new Vue({
  render: h => h(App),
  router: router,
  i18n: i18n,
}).$mount('#app')
