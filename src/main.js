// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import ElementUI from 'element-ui'
import 'element-ui/lib/theme-chalk/index.css'
import App from './App'
import router from './router'
import axios from 'axios'
import qs from 'qs'
import globalVariable from '@/global_var'
// import VueResource from 'vue-resource'
import './css/global.css'
import Vuex from 'vuex'

// require('./mock')

Vue.config.productionTip = false
Vue.prototype.GLOBAL = globalVariable

Vue.use(ElementUI)
// Vue.use(VueResource)
Vue.use(Vuex)

Vue.prototype.$http = axios
Vue.prototype.$axios = axios
Vue.prototype.$qs = qs
axios.defaults.baseURL = 'http://localhost:5000'

axios.defaults.headers.common['X-Requested-With'] = 'XMLHttpRequest'
axios.interceptors.request.use(
  config => {
    config.headers = {
      'Content-Type': 'application/json' //  注意：设置很关键
    }
    return config
  },
  err => {
    return Promise.reject(err)
  }
)
// axios.defaults.headers.post['Content-Type'] = 'application/x-www-form-urlencoded'
// axios.defaults.headers.get['Content-Type'] = 'application/x-www-form-urlencoded'

const store = new Vuex.Store({
  state: {
    count: 0,
    userList: [],
    username: '',
    authed: false,
    isAdmin: false
  },
  mutations: {
    increment (state) {
      state.count++
    },
    updateUserList (state, newUserList) {
      state.userList = newUserList
    },
    updateUsername (state, newUsername) {
      state.username = newUsername
      state.isAdmin = state.username === 'root'
    },
    updateAuth (state, authed) {
      state.authed = authed
    }
  }
})

/* eslint-disable no-new */
new Vue({
  el: '#app',
  store: store,
  router,
  components: { App },
  template: '<App/>'
})
