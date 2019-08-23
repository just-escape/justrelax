import Vue from 'vue'
import VueRouter from 'vue-router'

import PageHome from '@/components/PageHome.vue'
import PageEditor from '@/components/PageEditor.vue'
import PageRoom from '@/components/PageRoom.vue'
import PageScore from '@/components/PageScore.vue'
import PageStats from '@/components/PageStats.vue'

Vue.use(VueRouter)

const routes = [
  {path: '/', component: PageHome},
  {path: '/rooms/:room_id', component: PageRoom, props: true},
  {path: '/scores', component: PageScore},
  {path: '/stats', component: PageStats},
  {path: '/editor', component: PageEditor},
]

export default new VueRouter({
  routes,
  mode: "history"
})