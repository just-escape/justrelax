import Vue from 'vue'
import VueRouter from 'vue-router'

import PageRoot from '@/components/PageRoot.vue'

Vue.use(VueRouter)

const routes = [
  {path: '/', component: PageRoot},
]

export default new VueRouter({
  routes,
  mode: "history",
})
