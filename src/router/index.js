import Vue from 'vue'
import Router from 'vue-router'
import AuthRelationPage from '@/pages/relational/RelAuth'
import KnowRelationPage from '@/pages/relational/RelKnow'
import IsolateRelationPage from '@/pages/relational/RelIsolate'
import AuthGraphPage from '@/pages/graph/GraphAuth'
import KnowGraphPage from '@/pages/graph/GraphKnow'
import RelManipulation from '@/pages/relational/RelManipulation'
import NotFound from '@/pages/NotFound'

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
      path: '/relation/Isolate_2',
      name: '关系数据隔离',
      component: IsolateRelationPage
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
    },
    {
      path: '/404',
      name: '404页面',
      component: NotFound
    },
    {
      path: '/',
      redirect: '/relation/Auth_1' // 自动跳转
    },
    {
      path: '*',
      redirect: '/404' // 自动跳转，所有没有定义的都会自动跳转到Auth1
    }
  ]
})
