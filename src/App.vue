<template>
  <div id="app">
    <el-container v-if="loggedIn">
      <el-aside width="200px">
        <!-- left menu -->
        <el-menu
          default-active="relation"
          class="el-menu-vertical-demo"
          @select="selectVertical"
          background-color="#545c64"
          text-color="#fff"
          active-text-color="#ffd04b"
          style="height: 100%; margin-bottom: 50px; padding-top: 50px">
          <el-menu-item index="relation">
            <i class="el-icon-menu"></i>
            <span slot="title">关系数据服务</span>
          </el-menu-item>
          <el-menu-item index="graph">
            <i class="el-icon-menu"></i>
            <span slot="title">图数据服务</span>
          </el-menu-item>
          <el-menu-item index="other">
            <i class="el-icon-menu"></i>
            <span slot="title">……</span>
          </el-menu-item>
        </el-menu>
      </el-aside>
      <!-- right part -->
      <el-container>
        <el-main>
          <el-row style="height: 50px">
            <el-col :span="16">{{ this.GLOBAL.systemName }}</el-col>
            <el-col :span="8">
              <el-dropdown>
                <span class="el-dropdown-link">
                  <!--{{ userAdmin ? '管理员': '普通用户' }}/{{ userName }}<i class="el-icon-arrow-down el-icon&#45;&#45;right"></i>-->
                  {{ userName }}<i class="el-icon-arrow-down el-icon--right"></i>
                </span>
                <el-dropdown-menu slot="dropdown">
                  <el-dropdown-item icon="el-icon-plus">设置</el-dropdown-item>
                  <el-dropdown-item icon="el-icon-circle-plus">登出</el-dropdown-item>
                </el-dropdown-menu>
              </el-dropdown>
            </el-col>
          </el-row>
          <el-row>
            <el-col :span="12" style="margin-top: 10px">工业{{ getSubTitle() }}数据管理服务</el-col>
            <el-col :span="12">
              <el-button type="primary" plain @click="inputUserName=userName; authTableShow=true" v-if="!authed">身份认证</el-button>
              <el-button type="primary" plain @click="authed=false; document.cookie='authed='" v-else>取消认证</el-button>
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
          <!--          <div class="unable"></div>-->
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
    <el-dialog title="登录" v-if="!loggedIn" :visible.sync="showLogin">
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
      password: '',
      inputUserName: '',
      formLabelWidth: '80px',
      authed: false,
      loggedIn: false,
      showLogin: true
    }
  },
  methods: {
    selectVertical: function (index, indexPath) {
      this.activeDatabase = index
      console.log('Now active database: ', index)
      this.$router.push({path: '/' + this.activeDatabase + '/' + this.activePage, query: {}})
    },
    selectHorizontal: function (index, indexPath) {
      this.activePage = index
      console.log('Now active page: ', index)
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
    login: function () {
      let nowUsername = this.inputUserName // prevent the change of username during the request
      this.$http.post('/login/', {
        username: this.inputUserName,
        password: this.password
      }).then(
        function (response) {
          if (response.status === 200 && response.body.result === '登录成功') {
            console.log(response.body)
            if (response.body.usertype === '管理员') {
              this.userAdmin = true
            } else {
              this.userAdmin = false
            }
            this.userName = nowUsername
            this.GLOBAL.username = nowUsername
            document.cookie = 'username=' + nowUsername
            this.loggedIn = true
            this.showLogin = false
          } else {
            this.$alert('登录失败，请检查用户名与密码并稍后再试！')
          }
        }, function (response) {
          this.$alert('登录失败，请检查用户名与密码，检查网络连接，并稍后再试！')
        })
    },
    auth: function () {
      this.inputUserName = this.userName
      this.$http.post('/relational/authenticate/', {
        username: this.userName, // 不给他输入别的用户名的机会，就算是前端改了框里的内容也不让他提交（
        password: this.password
      }).then(
        function (response) {
          if (response.status === 200 && response.body.success) {
            console.log(response.body)
            this.authTableShow = false
            this.authed = true
            this.$alert(response.body.result)
            document.cookie = 'authed=true'
          } else {
            this.$alert('认证失败，请检查密码并稍后再试！')
          }
        }, function (response) {
          this.$alert('认证失败，请检查密码，检查网络连接，并稍后再试！')
        })
    },
    showLogs: function () {
      this.logs = []
      this.logTableShow = true
      this.$http.get('/relational/log').then(
        function (response) {
          if (response.status === 200 && response.body.success) {
            console.log(response.body)
            for (let t in response.body.result) {
              this.logs.push({
                'data': response.body.result[t],
                'index': t
              })
            }
          } else {
            this.$alert('获取日志失败，请稍后再试！')
          }
        }, function (response) {
          this.$alert('获取日志失败，请检查网络连接，稍后再试！')
        })
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
    this.activeDatabase = pathSplit[1]
    this.activePage = pathSplit[2]
    if (getCookie('authed')) {
      this.authed = true
    }
    if (getCookie('username')) {
      this.userName = getCookie('username')
      this.GLOBAL.username = getCookie('username')
      this.loggedIn = true
      this.showLogin = false
    }
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
  /*.unable {*/
  /*  position: fixed;*/
  /*  margin: 0;*/
  /*  background: rgba(255,255,255,.8);*/
  /*}*/
</style>
