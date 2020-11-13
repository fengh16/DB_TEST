import Vue from 'vue'
import Router from 'vue-router'
import AuthPage from '@/pages/Auth_1'

Vue.use(Router)

export default new Router({
  mode: 'history', // 这样就不会有#符号了
  routes: [
    {
      path: '/1',
      name: '权限管理',
      component: AuthPage
    }
  ]
})
