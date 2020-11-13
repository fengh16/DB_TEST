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
            <el-col :span="16">工业互联网可信服务数据管理测试子平台</el-col>
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
              <el-button type="primary" plain>身份认证</el-button>
              <el-button type="primary" plain>查看日志</el-button>
            </el-col>
          </el-row>
          <el-menu :default-active="$route.path" class="el-menu-demo" mode="horizontal" router>
            <el-menu-item index="1">权限管理</el-menu-item>
            <el-menu-item index="2">数据隔离</el-menu-item>
            <el-menu-item index="3">安全控制</el-menu-item>
            <el-menu-item index="4">可操作性</el-menu-item>
            <el-menu-item index="5">知情权</el-menu-item>
            <el-menu-item index="6">可迁移性</el-menu-item>
            <el-menu-item index="7">可恢复性</el-menu-item>
            <el-menu-item index="8">可销毁性</el-menu-item>
          </el-menu>
        </el-header>
        <el-main style="margin-top: 80px">
          <router-view/>
        </el-main>
      </el-container>
    </el-container>
  </div>
</template>

<script>
export default {
  name: 'App',
  data () {
    return {
      activeDatabase: 'relation',
      userAdmin: true,
      userName: '用户1'
    }
  },
  methods: {
    selectVertical: function (index, indexPath) {
      this.activeDatabase = index
      console.log('Now active database: ', index)
    },
    getSubTitle: function () {
      if (this.activeDatabase === 'relation') {
        return '关系'
      } else if (this.activeDatabase === 'graph') {
        return '图'
      }
      return '其他'
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
</style>
