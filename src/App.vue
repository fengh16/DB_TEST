<template>
  <div id="app">
    <el-container>
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
        <el-header style="margin-top: 20px">
          <!-- right top menu -->
          <el-row style="height: 50px">
            <el-col :span="16">{{ this.GLOBAL.systemName }}</el-col>
            <el-col :span="8">
              <el-dropdown>
                <span class="el-dropdown-link">
                  {{ userAdmin ? '管理员': '普通用户' }}/{{ userName }}<i class="el-icon-arrow-down el-icon--right"></i>
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
              <el-button type="primary" plain @click="authTableShow=true" v-if="!authed">身份认证</el-button>
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
        </el-header>
        <el-main style="margin-top: 80px">
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
          <el-input v-model="inputUserName" autocomplete="off" placeholder="请输入用户名"></el-input>
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
      authed: false
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
            this.$alert('登录成功！')
          } else {
            this.$alert('登录失败，请检查用户名与密码并稍后再试！')
          }
        }, function (response) {
          this.$alert('登录失败，请检查用户名与密码，检查网络连接，并稍后再试！')
        })
    },
    auth: function () {
      this.$http.post('/relational/authenticate/', {
        username: this.inputUserName,
        password: this.password
      }).then(
        function (response) {
          if (response.status === 200 && response.body.success) {
            console.log(response.body)
            this.authTableShow = false
            this.authed = true
            this.$alert(response.body.result)
          } else {
            this.$alert('认证失败，请检查用户名与密码并稍后再试！')
          }
        }, function (response) {
          this.$alert('认证失败，请检查用户名与密码，检查网络连接，并稍后再试！')
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
