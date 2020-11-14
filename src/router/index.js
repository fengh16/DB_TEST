import Vue from 'vue'
import Router from 'vue-router'
import AuthRelationPage from '@/pages/Auth_1_Relation'
import KnowRelationPage from '@/pages/Know_5_Relation'
import AuthGraphPage from '@/pages/Auth_1_Graph'
import KnowGraphPage from '@/pages/Know_5_Graph'
import RelManipulation from '@/pages/relational/RelManipulation'

Vue.use(Router)

export default new Router({
  mode: 'history', // 这样就不会有#符号了
  routes: [
    {
      path: '/relation/Auth_1',
      name: '关系权限管理',
      component: AuthRelationPage
    },
    {
      path: '/relation/Know_5',
      name: '关系知情权',
      component: KnowRelationPage
    },
    {
      path: '/graph/Auth_1',
      name: '图权限管理',
      component: AuthGraphPage
    },
    {
      path: '/graph/Know_5',
      name: '图知情权',
      component: KnowGraphPage
    },
    {
      path: '/relation/Operate_4',
      name: '关系可操作性',
      component: RelManipulation
    }
  ]
})
