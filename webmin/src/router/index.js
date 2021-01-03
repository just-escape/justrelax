import Vue from 'vue'
import VueRouter from 'vue-router'

import PageHome from '@/components/home/PageHome.vue'
import PageRuleSet from '@/components/editor/PageRuleSet.vue'
import PageLive from '@/components/live/PageLive.vue'
import PageScore from '@/components/score/PageScore.vue'
import PageStats from '@/components/stats/PageStats.vue'
// import PageSettings from '@/components/settings/PageSettings.vue'

Vue.use(VueRouter)

const routes = [
  {path: '/', component: PageHome},
  {path: '/rooms/:roomId/live', component: PageLive, props: true},
  {path: '/rooms/:roomId/scores', component: PageScore, props: true},
  {path: '/rooms/:roomId/stats', component: PageStats, props: true},
  {path: '/editor/:ruleSetId', component: PageRuleSet, props: true},
  // {path: '/rooms/:roomId/settings', component: PageSettings, props: true},
]

export default new VueRouter({
  routes,
  mode: "history",
})