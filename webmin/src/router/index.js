import Vue from 'vue'
import VueRouter from 'vue-router'

import PageHome from '@/components/home/PageHome.vue'
import PageEditor from '@/components/editor/PageEditor.vue'
import PageLive from '@/components/live/PageLive.vue'
import PageScore from '@/components/score/PageScore.vue'
import PageStats from '@/components/stats/PageStats.vue'
import PageSettings from '@/components/settings/PageSettings.vue'
import PageMedia from '@/components/media/PageMedia.vue'

Vue.use(VueRouter)

const routes = [
  {path: '/', component: PageHome},
  {path: '/rooms/:roomId/live', component: PageLive, props: true},
  {path: '/rooms/:roomId/scores', component: PageScore, props: true},
  {path: '/rooms/:roomId/stats', component: PageStats, props: true},
  {path: '/rooms/:roomId/editor', component: PageEditor, props: true},
  {path: '/rooms/:roomId/settings', component: PageSettings, props: true},
  {path: '/medias', component: PageMedia},
]

export default new VueRouter({
  routes,
  mode: "history",
})