<template>
  <div id="app">
    <el-container v-if="loggedIn" v-loading="appLogging">
      <el-header>
        <el-row type="flex" class="app-header-row">
          <el-col :span="16"><h2>{{ this.GLOBAL.systemName }}</h2></el-col>
          <el-col :span="8" style="text-align: center;">
            <el-dropdown @command="userCommand" style="position: relative; top: 50%; transform: translateY(-50%);">
                <span class="el-dropdown-link">
                  <!--{{ userAdmin ? '管理员': '普通用户' }}/{{ userName }}<i class="el-icon-arrow-down el-icon--right"></i>-->
                  {{ userName }}<i class="el-icon-arrow-down el-icon--right"></i>
                </span>
              <el-dropdown-menu slot="dropdown">
                <!--<el-dropdown-item icon="el-icon-plus" command="settings">设置</el-dropdown-item>-->
                <el-dropdown-item v-for="(username, i) in this.userList" :key="i" :command="i">{{username}}</el-dropdown-item>
                <el-dropdown-item icon="el-icon-circle-plus" command="logout">登出</el-dropdown-item>
              </el-dropdown-menu>
            </el-dropdown>

          </el-col>
        </el-row>
      </el-header>
      <el-container>
        <el-aside width="240px" class="app-sidebar">
          <!-- left menu -->
          <el-menu
            default-active="relation"
            class="el-menu-vertical-demo"
            @select="selectVertical"
            background-color="#ffffff"
            text-color="#404040"
            active-text-color="#409eff"
            style="height: 100%; margin-bottom: 50px; padding-top: 50px">
            <el-menu-item
              v-for="(item, i) in asideMenuItemProps"
              :key="i"
              :index="item.index"
              class="aside-menu-item">
              <template slot-scope="scope">
                <i class="el-icon-takeaway-box"></i>
                <span slot="title">{{item.title}}</span>
              </template>
            </el-menu-item>
          </el-menu>
        </el-aside>
        <el-main>
          <el-row>
            <el-col :span="12" style="margin-top: 10px"><h1>工业{{ getSubTitle() }}数据管理服务</h1></el-col>
            <el-col :span="12">
              <el-button type="primary" plain @click="doAuth" v-if="!authed">身份认证</el-button>
              <el-button type="primary" plain @click="cancelAuth" v-else>取消认证</el-button>
              <el-button type="primary" plain @click="doSetPassword" v-if="this.GLOBAL.username==='root'">设置密码</el-button>
              <el-button type="primary" plain @click="showLogs">查看日志</el-button>
            </el-col>
          </el-row>
          <el-menu :default-active="activePage" class="el-menu-demo" mode="horizontal" @select="selectHorizontal">
            <el-menu-item index="Auth_1">权限管理</el-menu-item>
            <el-menu-item index="Isolate_2">数据隔离</el-menu-item>
            <el-menu-item index="Control_3">安全控制</el-menu-item>
            <el-menu-item index="Operate_4">可操作性</el-menu-item>
            <el-menu-item index="Know_5">知情权</el-menu-item>
            <el-menu-item index="Migrate_6">可迁移性</el-menu-item>
            <el-menu-item index="Recover_7">可恢复性</el-menu-item>
            <el-menu-item index="Destroy_8">可销毁性</el-menu-item>
          </el-menu>
          <router-view v-if="authed"/>
          <h1 v-else>请先进行身份认证！</h1>
        </el-main>
      </el-container>
    </el-container>
    <el-dialog title="日志记录" :visible.sync="logTableShow">
      <el-table :data="logs">
        <el-table-column property="index" label="" width="40px"></el-table-column>
        <el-table-column property="data" label="记录"></el-table-column>
      </el-table>
    </el-dialog>
    <el-dialog title="身份认证" :visible.sync="authTableShow">
      <el-form>
        <el-form-item label="用户名" :label-width="formLabelWidth">
          <el-input v-model="inputUserName" autocomplete="off" placeholder="用户名" disabled></el-input>
        </el-form-item>
        <el-form-item label="密码" :label-width="formLabelWidth">
          <el-input v-model="password" autocomplete="off" placeholder="请输入密码" show-password></el-input>
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="authTableShow=false">取 消</el-button>
        <el-button type="primary" @click="this.auth">认 证</el-button>
      </div>
    </el-dialog>
    <el-dialog title="设置密码" :visible.sync="setPasswordTableShow">
      <el-form>
        <el-form-item label="用户名" :label-width="formLabelWidth">
          <el-input v-model="setPasswordUsername" autocomplete="off" placeholder="用户名" disabled></el-input>
        </el-form-item>
        <el-form-item label="密码" :label-width="formLabelWidth">
          <el-input v-model="newPassword" autocomplete="off" placeholder="请输入密码" show-password></el-input>
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="setPasswordTableShow=false">取 消</el-button>
        <el-button type="primary" @click="this.setPassword">提 交</el-button>
      </div>
    </el-dialog>
    <el-dialog title="工业互联网工业互联网可信服务数据管理测试平台" v-if="!loggedIn" :visible.sync="showLogin" :close-on-click-modal=false :close-on-press-escape=false :show-close=false>
      <h3>登 录</h3>
      <el-form>
        <el-form-item label="用户名" :label-width="formLabelWidth">
          <el-input v-model="inputUserName" autocomplete="off" placeholder="请输入用户名"></el-input>
        </el-form-item>
        <el-form-item label="密码" :label-width="formLabelWidth">
          <el-input v-model="password" autocomplete="off" placeholder="请输入密码" show-password></el-input>
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button type="primary" @click="this.login">登 录</el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
export default {
  name: 'App',
  data () {
    return {
      activeDatabase: 'relation',
      activePage: 'Auth_1',
      userAdmin: true,
      userName: this.GLOBAL.username,
      logs: [],
      logTableShow: false,
      authTableShow: false,
      setPasswordTableShow: false,
      password: '',
      inputUserName: '',
      setPasswordUsername: '',
      formLabelWidth: '80px',
      authed: false,
      loggedIn: false,
      showLogin: true,
      appLogging: false,
      newPassword: '',
      userList: ['root', 'developer1', 'developer2', 'developer3', 'developer4'],
      asideMenuItemProps: [{
        index: 'relation',
        title: '关系数据管理服务'
      }, {
        index: 'graph',
        title: '图数据管理服务'
      }, {
        index: 'timeSeries',
        title: '时序数据管理服务'
      }, {
        index: 'document',
        title: '文档数据管理服务'
      }, {
        index: 'columnOriented',
        title: '列式数据管理服务'
      }, {
        index: 'keyValue',
        title: '键值对数据管理服务'
      }, {
        index: 'event',
        title: '事件数据管理服务'
      }, {
        index: 'message',
        title: '消息队列数据管理服务'
      }, {
        index: 'blob',
        title: '二进制大对象数据管理服务'
      }]
    }
  },
  methods: {
    selectVertical: function (index, indexPath) {
      this.activeDatabase = index
      console.log('Now active database: ', index)
      if (!this.activePage) {
        this.activePage = 'Auth_1'
      }
      this.$router.push({path: '/' + this.activeDatabase + '/' + this.activePage, query: {}})
    },
    selectHorizontal: function (index, indexPath) {
      this.activePage = index
      console.log('Now active page: ', index)
      if (!this.activeDatabase) {
        this.activeDatabase = 'relation'
      }
      this.$router.push({path: '/' + this.activeDatabase + '/' + this.activePage, query: {}})
    },
    getSubTitle: function () {
      if (this.activeDatabase === 'relation') {
        return '关系'
      } else if (this.activeDatabase === 'graph') {
        return '图'
      }
      return '其他'
    },
    showAuth: function () {
      this.password = ''
      this.authTableShow = true
    },
    doLogout: function () {
      console.log('HHH')
      this.authed = false
      this.loggedIn = false
      document.cookie = 'username='
      document.cookie = 'authed='
      this.userName = ''
      this.GLOBAL.username = ''
      this.showLogin = true
    },
    login: function () {
      let nowUsername = this.inputUserName // prevent the change of username during the request
      this.appLogging = true
      let _this = this
      this.$http.post('/login/', {
        username: this.inputUserName,
        password: this.password
      }).then(
        function (response) {
          if (response.status === 200 && response.data.result === '登录成功') {
            console.log(response.data)
            if (response.data.usertype === '管理员') {
              _this.userAdmin = true
              localStorage.setItem('isAdmin', 'true')
              _this.GLOBAL.isAdmin = true
            } else {
              _this.userAdmin = false
              localStorage.setItem('isAdmin', 'false')
              _this.GLOBAL.isAdmin = false
            }
            _this.userName = nowUsername
            _this.GLOBAL.username = nowUsername
            localStorage.setItem('username', nowUsername)
            _this.$store.commit('updateUsername', nowUsername)
            document.cookie = 'username=' + nowUsername
            _this.loggedIn = true
            _this.showLogin = false

            _this.getUserList()
          } else {
            _this.$alert('登录失败，请检查用户名与密码并稍后再试！')
          }
          _this.appLogging = false
        }, function (response) {
          _this.$alert('登录失败，请检查用户名与密码，检查网络连接，并稍后再试！')
          _this.appLogging = false
        })
    },
    doSetPassword: function () {
      this.setPasswordUsername = this.$store.state.username
      this.setPasswordUsername = localStorage.getItem('username')
      this.setPasswordTableShow = true
    },
    doAuth: function () {
      this.inputUserName = this.userName
      this.authTableShow = true
    },
    cancelAuth: function () {
      this.authed = false
      document.cookie = 'authed='
    },
    setPassword: function () {
      let _this = this
      this.$http.post('/set-password/', {
        username: this.setPasswordUsername,
        password: this.newPassword
      }).then(response => {
        if (response.status === 200 && response.data.success) {
          _this.setPasswordTableShow = false
          _this.$alert('设置成功')
        } else {
          _this.setPasswordTableShow = false
          _this.$alert(`设置失败：${response.data.msg}`)
        }
      }, response => {
        _this.$alert('设置失败，请检查网络连接，并稍后再试！')
      })
    },
    auth: function () {
      let _this = this
      this.inputUserName = this.userName
      this.$http.post('/relational/authenticate/', {
        username: this.userName, // 不给他输入别的用户名的机会，就算是前端改了框里的内容也不让他提交（
        password: this.password
      }).then(
        function (response) {
          if (response.status === 200 && response.data.success) {
            console.log(response.data)
            _this.authTableShow = false
            _this.authed = true
            localStorage.setItem('authed', 'true')
            _this.$store.commit('updateAuth', true)
            _this.$alert(response.data.result)
            document.cookie = 'authed=true'
          } else {
            localStorage.setItem('authed', 'false')
            _this.$store.commit('updateAuth', false)
            _this.$alert('认证失败，请检查密码并稍后再试！')
          }
        }, function (response) {
          _this.$alert('认证失败，请检查密码，检查网络连接，并稍后再试！')
        })
    },
    showLogs: function () {
      let _this = this
      this.logs = []
      this.logTableShow = true
      this.$http.get('/relational/log/').then(
        function (response) {
          if (response.status === 200 && response.data.success) {
            console.log(response.data)
            for (let t in response.data.result) {
              _this.logs.push({
                'data': response.data.result[t],
                'index': t
              })
            }
          } else {
            _this.$alert('获取日志失败，请稍后再试！')
          }
        }, function (response) {
          _this.$alert('获取日志失败，请检查网络连接，稍后再试！')
        })
    },
    changeUser (userIndex) {
      let newUsername = this.userList[userIndex]
      let password = newUsername
      this.authed = false
      this.loggedIn = false
      document.cookie = 'username='
      document.cookie = 'authed='
      this.userName = ''
      this.GLOBAL.username = ''
      this.showLogin = false
      this.appLogging = true
      let _this = this
      this.$http.post('/change-user/', {
        username: newUsername,
        password: password
      }).then((response) => {
        if (response.status === 200 && response.data.result === '登录成功') {
          if (response.data.usertype === '管理员') {
            localStorage.setItem('isAdmin', 'true')
            this.GLOBAL.isAdmin = true
            _this.userAdmin = true
          } else {
            localStorage.setItem('isAdmin', 'false')
            this.GLOBAL.isAdmin = false
            _this.userAdmin = false
          }
          _this.userName = newUsername
          // _this.password = password
          _this.GLOBAL.username = newUsername
          localStorage.setItem('username', newUsername)
          _this.$store.commit('updateUsername', newUsername)
          document.cookie = 'username=' + newUsername
          _this.loggedIn = true
          _this.showLogin = false
          console.log(this.userName, this.password)
        } else {
          _this.$alert('登录失败，请检查用户名与密码并稍后再试！')
        }
        _this.appLogging = false
      }, (response) => {
        _this.$alert('登录失败，请检查用户名与密码，检查网络连接，并稍后再试！')
        _this.appLogging = false
      })
    },
    userCommand (item) {
      if (item === 'logout') {
        this.doLogout()
      } else {
        this.changeUser(parseInt(item))
      }
    },
    getUserList () {
      let _this = this
      this.$http.get('/relational/user-list/', {
        params: {
          username: this.userName
        }
      }).then(
        function (response) {
          if (response.status === 200 && response.data.success) {
            console.log(response.data)
            // _this.userList = response.data.result
            _this.GLOBAL.userList = response.data.result
            localStorage.setItem('userList', JSON.stringify(response.data.result))
            _this.readUserListFromLocalStorage()
            _this.$store.commit('updateUserList', response.data.result)
          } else {
            _this.$alert(`获取用户列表失败：${response.data.msg}`)
          }
        }, function (response) {
          _this.$alert('获取用户列表失败，请检查网络连接，稍后再试！')
        })
    },
    readUserListFromLocalStorage () {
      this.userList = JSON.parse(localStorage.getItem('userList'))
    }
  },
  created () {
    function getCookie (cname) {
      var name = cname + '='
      var ca = document.cookie.split(';')
      for (var i = 0; i < ca.length; i++) {
        var c = ca[i].trim()
        if (c.indexOf(name) === 0) return c.substring(name.length, c.length)
      }
      return ''
    }
    let pathSplit = this.$route.path.split('?')[0].split('/')
    this.activeDatabase = pathSplit.length > 2 ? pathSplit[1] : ''
    this.activePage = pathSplit.length > 2 ? pathSplit[2] : ''
    if (getCookie('authed')) {
      this.authed = true
    }
    if (getCookie('username')) {
      this.userName = getCookie('username')
      this.GLOBAL.username = getCookie('username')
      this.loggedIn = true
      this.showLogin = false
    }
    this.readUserListFromLocalStorage()
    this.GLOBAL.userName = localStorage.getItem('username')
    this.GLOBAL.userList = JSON.parse(localStorage.getItem('userList'))
    this.GLOBAL.isAdmin = JSON.parse(localStorage.getItem('isAdmin'))
  }
}
</script>

<style>
  #app {
    font-family: 'Avenir', Helvetica, Arial, sans-serif;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    text-align: center;
    color: #2c3e50;
    /*margin-top: 60px;*/
  }
  .app-sidebar {
    /*display: block;*/
    height: 100vh;
    position: relative;
    overflow-y: hidden;
  }
  .app-sidebar ul {
    padding-top: 0 !important;
  }
  .aside-menu-item {
    text-align: left;
  }
  .el-dropdown-link {
    cursor: pointer;
    color: #f0f0f0;
  }
  .el-dropdown-link:hover {
    color: #409eff;
  }
  /*.app-header-row {*/
  /*  background-color: #212529;*/
  /*}*/
  .el-header {
    height: 70px !important;
    background-color: #545c68;
  }
  .el-header h2 {
    color: #f0f0f0;
  }
  /*.unable {*/
  /*  position: fixed;*/
  /*  margin: 0;*/
  /*  background: rgba(255,255,255,.8);*/
  /*}*/
</style>
