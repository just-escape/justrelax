import Vue from 'vue'
import VueRouter from 'vue-router'

import PageHome from '@/components/PageHome.vue'
import PageEditor from '@/components/PageEditor.vue'
import PageLive from '@/components/PageLive.vue'
import PageScore from '@/components/PageScore.vue'
import PageStats from '@/components/PageStats.vue'
import PageSettings from '@/components/PageSettings.vue'

Vue.use(VueRouter)

const routes = [
  {path: '/', component: PageHome},
  {path: '/rooms/:roomId/live', component: PageLive, props: true},
  {path: '/rooms/:roomId/scores', component: PageScore, props: true},
  {path: '/rooms/:roomId/stats', component: PageStats, props: true},
  {path: '/rooms/:roomId/editor', component: PageEditor, props: true},
  {path: '/rooms/:roomId/settings', component: PageSettings, props: true},
]

export default new VueRouter({
  routes,
  mode: "history"
})