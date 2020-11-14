import Vue from 'vue'
import Router from 'vue-router'
import AuthRelationPage from '@/pages/relational/RelAuth'
import KnowRelationPage from '@/pages/relational/RelKnow'
import IsolateRelationPage from '@/pages/relational/RelIsolate'
import AuthGraphPage from '@/pages/graph/GraphAuth'
import KnowGraphPage from '@/pages/graph/GraphKnow'
import RelManipulation from '@/pages/relational/RelManipulation'
import RelMigration from '@/pages/relational/RelMigration'
import RelRecover from '@/pages/relational/RelRecover'
import RelDestroy from '@/pages/relational/RelDestroy'
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
      path: '/relation/Migrate_6',
      name: '关系可迁移性',
      component: RelMigration
    },
    {
      path: '/relation/Recover_7',
      name: '关系可恢复性',
      component: RelRecover
    },
    {
      path: '/relation/Destroy_8',
      name: '关系可销毁性',
      component: RelDestroy
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
