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

// require('./mock')

Vue.config.productionTip = false
Vue.prototype.GLOBAL = globalVariable

Vue.use(ElementUI)
// Vue.use(VueResource)

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

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  components: { App },
  template: '<App/>'
})
