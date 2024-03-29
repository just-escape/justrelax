import Vue from 'vue'
import axios from 'axios'
import VueAxios from 'vue-axios'
import VueNativeSock from 'vue-native-websocket'
import VueAnime from 'vue-animejs'
import BootstrapVue from 'bootstrap-vue'
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'

import publishSubscribeService from '@/store/publishSubscribeService.js'
import router from '@/router/index.js'

import App from '@/App.vue'

Vue.use(VueAxios, axios)
Vue.use(VueNativeSock, 'ws://localhost:3031', {
  store: publishSubscribeService,
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
}).$mount('#app')
