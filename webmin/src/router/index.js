import Vue from 'vue'
import VueRouter from 'vue-router'

import PageHome from '@/components/home/PageHome.vue'
import PageLive from '@/components/live/PageLive.vue'

Vue.use(VueRouter)

const routes = [
  {path: '/', component: PageHome},
  {path: '/rooms/:roomId/live', component: PageLive, props: true},
]

export default new VueRouter({
  routes,
  mode: "history",
})